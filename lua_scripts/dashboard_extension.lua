--[[
    Assetto Corsa Telemetry Dashboard Extension
    Main Lua script for in-game integration
    
    Installation:
    1. Copy this file to: assettocorsa/apps/lua/dashboard_extension/
    2. Enable the app in AC's settings
]]

-- App information
local appName = "AC Telemetry Dashboard"
local appVersion = "1.0.0"

-- Configuration
local config = {
    udp_host = "127.0.0.1",
    udp_port = 9996,
    control_port = 9997,
    update_rate = 20, -- Hz
    debug_mode = false
}

-- State variables
local isInitialized = false
local lastUpdate = 0
local updateInterval = 1.0 / config.update_rate
local udpSocket = nil
local controlSocket = nil

-- Telemetry data structure
local telemetryData = {
    -- Basic vehicle data
    speed_kmh = 0,
    speed_mph = 0,
    rpm = 0,
    max_rpm = 8000,
    gear = 0,
    
    -- G-forces
    g_force_lateral = 0,
    g_force_longitudinal = 0,
    g_force_vertical = 0,
    
    -- Lap data
    lap_time = 0,
    last_lap = 0,
    best_lap = 0,
    lap_count = 0,
    
    -- Fuel and temperatures
    fuel = 0,
    water_temp = 0,
    oil_temp = 0,
    oil_pressure = 0,
    
    -- Tire data (FL, FR, RL, RR)
    tire_pressure = {0, 0, 0, 0},
    tire_temperature_core = {0, 0, 0, 0},
    tire_temperature_inner = {0, 0, 0, 0},
    tire_temperature_middle = {0, 0, 0, 0},
    tire_temperature_outer = {0, 0, 0, 0},
    tire_wear = {100, 100, 100, 100},
    
    -- Suspension and wheels
    suspension_travel = {0, 0, 0, 0},
    wheel_load = {0, 0, 0, 0},
    wheel_angular_speed = {0, 0, 0, 0},
    wheel_slip = {0, 0, 0, 0},
    
    -- Vehicle dynamics
    car_position = {0, 0, 0},
    car_velocity = {0, 0, 0},
    car_acceleration = {0, 0, 0},
    
    -- Electronics and controls
    tc_setting = 0,
    tc_in_action = false,
    abs_setting = 0,
    abs_in_action = false,
    brake_bias = 0.5,
    
    -- Flags
    pit_limiter_on = false,
    in_pit = false,
    engine_map = 1,
    
    -- Additional data
    turbo_pressure = 0,
    engine_load = 0
}

-- Control command handlers
local controlHandlers = {
    [1] = function(value) -- TC_LEVEL
        if value >= 0 and value <= 10 then
            ac.setTractionControl(value)
            if config.debug_mode then
                ac.log("Dashboard: Set TC level to " .. value)
            end
        end
    end,
    
    [2] = function(value) -- ABS_LEVEL
        if value >= 0 and value <= 10 then
            ac.setABS(value)
            if config.debug_mode then
                ac.log("Dashboard: Set ABS level to " .. value)
            end
        end
    end,
    
    [3] = function(value) -- BRAKE_BIAS
        if value >= 0.0 and value <= 1.0 then
            -- Note: AC's brake bias control may be limited depending on car
            if config.debug_mode then
                ac.log("Dashboard: Brake bias adjustment requested: " .. value)
            end
        end
    end,
    
    [5] = function(value) -- HEADLIGHTS
        ac.setHeadlights(value and 1 or 0)
        if config.debug_mode then
            ac.log("Dashboard: Headlights " .. (value and "on" or "off"))
        end
    end,
    
    [6] = function(value) -- LEFT_INDICATOR
        ac.setTurnIndicator(value and -1 or 0)
        if config.debug_mode then
            ac.log("Dashboard: Left indicator " .. (value and "on" or "off"))
        end
    end,
    
    [7] = function(value) -- RIGHT_INDICATOR
        ac.setTurnIndicator(value and 1 or 0)
        if config.debug_mode then
            ac.log("Dashboard: Right indicator " .. (value and "on" or "off"))
        end
    end,
    
    [8] = function(value) -- HAZARD_LIGHTS
        ac.setHazardLights(value and 1 or 0)
        if config.debug_mode then
            ac.log("Dashboard: Hazard lights " .. (value and "on" or "off"))
        end
    end,
    
    [9] = function(value) -- WIPERS
        ac.setWipers(value and 1 or 0)
        if config.debug_mode then
            ac.log("Dashboard: Wipers " .. (value and "on" or "off"))
        end
    end,
    
    [10] = function(value) -- PIT_LIMITER
        ac.setPitLimiter(value and 1 or 0)
        if config.debug_mode then
            ac.log("Dashboard: Pit limiter " .. (value and "on" or "off"))
        end
    end
}

-- Initialize the app
function script.prepare(dt)
    if not isInitialized then
        -- Log initialization
        ac.log("Initializing " .. appName .. " v" .. appVersion)
        
        -- Setup UDP sockets (conceptual - AC Lua doesn't have direct UDP support)
        -- In practice, this would use AC's built-in UDP telemetry or shared memory
        
        -- Load configuration if available
        loadConfiguration()
        
        isInitialized = true
        ac.log("Dashboard extension initialized successfully")
    end
end

-- Main update loop
function script.update(dt)
    if not isInitialized then
        return
    end
    
    -- Update timing
    lastUpdate = lastUpdate + dt
    
    -- Send telemetry data at specified rate
    if lastUpdate >= updateInterval then
        updateTelemetryData()
        sendTelemetryData()
        lastUpdate = 0
    end
    
    -- Process control commands
    processControlCommands()
end

-- Update telemetry data from AC
function updateTelemetryData()
    -- Get car state
    local car = ac.getCar(0) -- Player car
    if not car then return end
    
    -- Basic vehicle data
    telemetryData.speed_kmh = car.speedKmh
    telemetryData.speed_mph = car.speedKmh * 0.621371
    telemetryData.rpm = car.rpm
    telemetryData.max_rpm = car.rpmLimiter
    telemetryData.gear = car.gear
    
    -- G-forces
    telemetryData.g_force_lateral = car.gForces.x
    telemetryData.g_force_longitudinal = car.gForces.z
    telemetryData.g_force_vertical = car.gForces.y
    
    -- Position and velocity
    telemetryData.car_position = {car.position.x, car.position.y, car.position.z}
    telemetryData.car_velocity = {car.velocity.x, car.velocity.y, car.velocity.z}
    telemetryData.car_acceleration = {car.acceleration.x, car.acceleration.y, car.acceleration.z}
    
    -- Lap data
    telemetryData.lap_time = car.lapTime
    telemetryData.last_lap = car.lastLap
    telemetryData.best_lap = car.bestLap
    telemetryData.lap_count = car.lapCount
    
    -- Fuel and temperatures
    telemetryData.fuel = car.fuel
    telemetryData.water_temp = car.waterTemperature
    telemetryData.oil_temp = car.oilTemperature
    
    -- Tire data
    for i = 0, 3 do
        telemetryData.tire_pressure[i + 1] = car.wheels[i].tyrePressure
        telemetryData.tire_temperature_core[i + 1] = car.wheels[i].tyreTemperature[1] -- Core temp
        telemetryData.tire_temperature_inner[i + 1] = car.wheels[i].tyreTemperature[0] -- Inner
        telemetryData.tire_temperature_middle[i + 1] = car.wheels[i].tyreTemperature[1] -- Middle
        telemetryData.tire_temperature_outer[i + 1] = car.wheels[i].tyreTemperature[2] -- Outer
        telemetryData.tire_wear[i + 1] = (1.0 - car.wheels[i].tyreWear) * 100 -- Convert to percentage
        
        -- Suspension and wheel data
        telemetryData.suspension_travel[i + 1] = car.wheels[i].suspensionTravel
        telemetryData.wheel_load[i + 1] = car.wheels[i].load
        telemetryData.wheel_angular_speed[i + 1] = car.wheels[i].angularSpeed
        telemetryData.wheel_slip[i + 1] = car.wheels[i].slipRatio
    end
    
    -- Electronics
    telemetryData.tc_setting = car.tractionControl
    telemetryData.tc_in_action = car.tractionControlInAction
    telemetryData.abs_setting = car.abs
    telemetryData.abs_in_action = car.absInAction
    
    -- Additional data
    telemetryData.turbo_pressure = car.turboBoost
    telemetryData.pit_limiter_on = car.pitLimiterOn
    telemetryData.in_pit = car.isInPitlane
    
    -- Calculate brake bias (if available)
    -- This might not be directly available in AC's API
    telemetryData.brake_bias = 0.5 -- Default to 50/50
end

-- Send telemetry data via UDP (conceptual)
function sendTelemetryData()
    -- In a real implementation, this would:
    -- 1. Serialize telemetryData to binary format
    -- 2. Send via UDP to the dashboard application
    -- 3. Handle any network errors
    
    -- For now, we'll use AC's shared memory or file output
    -- This is a placeholder for the actual UDP implementation
    
    if config.debug_mode then
        -- Log some key data for debugging
        ac.log(string.format("Dashboard: Speed=%.1f km/h, RPM=%d, Gear=%d", 
               telemetryData.speed_kmh, telemetryData.rpm, telemetryData.gear))
    end
end

-- Process incoming control commands
function processControlCommands()
    -- In a real implementation, this would:
    -- 1. Listen for UDP packets on the control port
    -- 2. Parse command packets
    -- 3. Execute the appropriate control action
    
    -- This is a placeholder for the actual control implementation
end

-- Load configuration from file
function loadConfiguration()
    -- Try to load configuration from a file
    -- AC Lua has limited file I/O, so this might use AC's settings system
    
    local configFile = ac.getFolder(ac.FolderID.Documents) .. "/Assetto Corsa/cfg/dashboard_extension.ini"
    
    -- In a real implementation, parse INI file and update config table
    -- For now, use defaults
    
    if config.debug_mode then
        ac.log("Dashboard: Configuration loaded")
    end
end

-- Handle app window drawing (if GUI is needed)
function script.drawUI()
    -- This could draw a simple status window in AC
    -- For now, keep it minimal since the main UI is external
    
    if ac.isWindowOpen("Dashboard Status") then
        ac.beginWindow("Dashboard Status", vec2(200, 100))
        
        ac.text("AC Telemetry Dashboard")
        ac.text("Status: " .. (isInitialized and "Running" or "Initializing"))
        ac.text("Update Rate: " .. config.update_rate .. " Hz")
        
        if ac.button("Close") then
            ac.setWindowOpen("Dashboard Status", false)
        end
        
        ac.endWindow()
    end
end

-- Cleanup when app is closed
function script.windowMain()
    -- Cleanup resources
    if udpSocket then
        -- Close UDP socket
        udpSocket = nil
    end
    
    if controlSocket then
        -- Close control socket
        controlSocket = nil
    end
    
    ac.log("Dashboard extension shutting down")
end

-- Handle CSP extended telemetry (if available)
function getExtendedTelemetry()
    -- This function would interface with CSP's extended telemetry
    -- CSP provides additional channels not available in base AC
    
    if ac.getCSPVersion and ac.getCSPVersion() > 0 then
        -- CSP is available, get extended data
        -- This would include things like:
        -- - Live brake bias adjustments
        -- - Differential settings
        -- - Turbo wastegate position
        -- - DRS status
        -- - KERS/ERS data
        
        if config.debug_mode then
            ac.log("Dashboard: CSP extended telemetry available")
        end
    end
end

-- Utility function to format time
function formatTime(seconds)
    if seconds <= 0 then
        return "00:00.000"
    end
    
    local minutes = math.floor(seconds / 60)
    local secs = seconds % 60
    
    return string.format("%02d:%06.3f", minutes, secs)
end

-- Export functions for external access (if needed)
dashboard = {
    getTelemetryData = function() return telemetryData end,
    getConfig = function() return config end,
    setConfig = function(newConfig) 
        for k, v in pairs(newConfig) do
            config[k] = v
        end
    end,
    isInitialized = function() return isInitialized end
}

-- Log successful load
ac.log("Dashboard extension Lua script loaded successfully")
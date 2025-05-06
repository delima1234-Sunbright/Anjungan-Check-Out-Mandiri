[
    {
        "id": "51a3ed2dba2ee22d",
        "type": "mqtt in",
        "z": "weather_dashboard_flow",
        "name": "MQTT weather/station_data",
        "topic": "weather/station_data",
        "qos": "2",
        "datatype": "auto-detect",
        "broker": "1498bfb91f583e3e",
        "nl": false,
        "rap": true,
        "rh": 0,
        "inputs": 0,
        "x": 160,
        "y": 480,
        "wires": [
            [
                "58ffb9dcbdc8447b"
            ]
        ]
    },
    {
        "id": "58ffb9dcbdc8447b",
        "type": "function",
        "z": "weather_dashboard_flow",
        "name": "Parse MQTT JSON & Add Timestamp",
        "func": "let data = msg.payload;\n\n// Jika payload adalah buffer, konversi ke string\nif (Buffer.isBuffer(data)) {\n    data = data.toString();\n}\n\n// Jika payload adalah string, parse ke JSON\nif (typeof data === 'string') {\n    try {\n        data = JSON.parse(data);\n    } catch (e) {\n        node.error(\"Failed to parse MQTT JSON: \" + e, msg);\n        return null; // Stop processing if JSON is invalid\n    }\n}\n\n// Pastikan data adalah objek\nif (typeof data !== 'object' || data === null) {\n    node.warn(\"Received non-object MQTT data\", msg);\n    return null;\n}\n\n// Buat objek baru dengan nilai yang di-parse ke number\n// Tambahkan penanganan jika properti tidak ada atau null\nconst parseFloatOrNull = (val) => {\n    const num = parseFloat(val);\n    return isNaN(num) ? null : num;\n};\n\nmsg.payload = {\n    timestamp: new Date().toISOString(),\n    temperature: parseFloatOrNull(data.temperature),\n    humidity: parseFloatOrNull(data.humidity),\n    heat_index: parseFloatOrNull(data.heat_index),\n    wind_speed_mps: parseFloatOrNull(data.wind_speed_mps),\n    wind_direction: parseFloatOrNull(data.wind_direction),\n    rain_value: parseFloatOrNull(data.rain_value),\n    pm25: parseFloatOrNull(data.pm25),\n    pressure: parseFloatOrNull(data.pressure)\n};\n\nreturn msg;",
        "outputs": 1,
        "timeout": 0,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 480,
        "y": 480,
        "wires": [
            [
                "18ba396b0cf29232",
                "1bc0f484ab7594e3"
            ]
        ]
    },
    {
        "id": "18ba396b0cf29232",
        "type": "change",
        "z": "weather_dashboard_flow",
        "name": "Store Latest Data in Flow Context",
        "rules": [
            {
                "t": "set",
                "p": "latestWeatherData",
                "pt": "flow",
                "to": "payload",
                "tot": "msg"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 800,
        "y": 440,
        "wires": [
            []
        ]
    },
    {
        "id": "1bc0f484ab7594e3",
        "type": "websocket out",
        "z": "weather_dashboard_flow",
        "name": "WS out /ws/weather",
        "server": "7e3e0898da3593ac",
        "client": "",
        "x": 820,
        "y": 500,
        "wires": []
    },
    {
        "id": "a3edcf8151d231d7",
        "type": "http in",
        "z": "weather_dashboard_flow",
        "name": "GET /api/weather/current",
        "url": "/api/weather/current",
        "method": "get",
        "upload": false,
        "swaggerDoc": "",
        "x": 220,
        "y": 560,
        "wires": [
            [
                "11211ec53b0cf3e4"
            ]
        ]
    },
    {
        "id": "11211ec53b0cf3e4",
        "type": "change",
        "z": "weather_dashboard_flow",
        "name": "Get Latest Data from Flow Context",
        "rules": [
            {
                "t": "set",
                "p": "payload",
                "pt": "msg",
                "to": "latestWeatherData",
                "tot": "flow"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 520,
        "y": 560,
        "wires": [
            [
                "e84f8abb901f030a"
            ]
        ]
    },
    {
        "id": "e84f8abb901f030a",
        "type": "http response",
        "z": "weather_dashboard_flow",
        "name": "Current API Response",
        "statusCode": "200",
        "headers": {
            "Content-Type": "application/json"
        },
        "x": 810,
        "y": 560,
        "wires": []
    },
    {
        "id": "0f7ae4bf21d735cd",
        "type": "http in",
        "z": "weather_dashboard_flow",
        "name": "GET /weather",
        "url": "/weather",
        "method": "get",
        "upload": false,
        "swaggerDoc": "",
        "x": 170,
        "y": 400,
        "wires": [
            [
                "d49a05a230e10a04"
            ]
        ]
    },
    {
        "id": "d49a05a230e10a04",
        "type": "template",
        "z": "weather_dashboard_flow",
        "name": "Main Weather Page HTML/CSS/JS",
        "field": "payload",
        "fieldType": "msg",
        "format": "html",
        "syntax": "mustache",
        "template": "<!DOCTYPE html>\n<html lang=\"en\">\n\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>CloudNex Weather Station Dashboard</title>\n    <link href=\"https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap\" rel=\"stylesheet\">\n    <style>\n        * {\n            margin: 0;\n            padding: 0;\n            box-sizing: border-box;\n            font-family: 'Poppins', sans-serif;\n        }\n\n        body {\n            background-color: #06283d;\n            color: #ffffff;\n            overflow-x: hidden;\n        }\n\n        .dashboard-container {\n            display: flex;\n            min-height: 100vh;\n        }\n\n        .sidebar {\n            width: 240px;\n            background-color: #dff6ff;\n            padding: 20px;\n            display: flex;\n            flex-direction: column;\n            align-items: center;\n        }\n\n        .logo {\n            margin-bottom: 40px;\n            text-align: center;\n        }\n\n        .logo img {\n            width: 120px;\n            height: auto;\n        }\n\n        .logo-text {\n            font-size: 14px;\n            color: #06283d;\n            margin-top: 5px;\n        }\n\n        .nav-items {\n            width: 100%;\n        }\n\n        .nav-item {\n            display: flex;\n            align-items: center;\n            width: 100%;\n            padding: 12px 15px;\n            margin-bottom: 10px;\n            border-radius: 8px;\n            color: #06283d;\n            text-decoration: none;\n            transition: background-color 0.3s;\n        }\n\n        .nav-item:hover:not(.active) {\n            background-color: rgba(6, 40, 61, 0.1);\n        }\n\n        .nav-icon {\n            margin-right: 12px;\n            width: 20px;\n            height: 20px;\n        }\n\n        .main-content {\n            flex: 1;\n            padding: 30px;\n            background-color: #06283d;\n        }\n\n        .header {\n            display: flex;\n            justify-content: space-between;\n            margin-bottom: 40px;\n        }\n\n        .date-section h1 {\n            font-size: 36px;\n            font-weight: 700;\n        }\n\n        .date-section p {\n            color: #94a3b8;\n            font-size: 16px;\n        }\n\n        .station-info {\n            text-align: right;\n        }\n\n        .station-info h1 {\n            font-size: 32px;\n            font-weight: 700;\n        }\n\n        .station-info p {\n            color: #94a3b8;\n            font-size: 16px;\n        }\n\n        .section-header {\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            margin-bottom: 20px;\n        }\n\n        .section-header h2 {\n            font-size: 24px;\n            font-weight: 600;\njavax: none;
        }\n\n        .section-header a {\n            color: #94a3b8;\n            text-decoration: none;\n            font-size: 14px;\n        }\n\n        .section-header a:hover {\n            color: #ffffff;\n        }\n\n        .weather-cards {\n            display: grid;\n            grid-template-columns: repeat(3, 1fr);\n            gap: 20px;\n            margin-bottom: 30px;\n        }\n\n        .weather-card {\n            background-color: #dff6ff;\n            border-radius: 16px;\n            padding: 20px;\n            color: #06283d;\n        }\n\n        .card-title {\n            color: #06283d;\n            font-size: 16px;\n            margin-bottom: 10px;\n            display: flex;\n            align-items: center;\n        }\n\n        .card-title svg {\n            margin-right: 8px;\n        }\n\n        .card-value {\n            font-size: 32px;\n            font-weight: 700;\n        }\n\n        .card-value.loading::after {\n            content: \"...\";\n        }\n\n        .map-container {\n            width: 100%;\n            height: 300px;\n            border-radius: 16px;\n            overflow: hidden;\n            margin-bottom: 30px;\n        }\n\n        .map-container iframe {\n            width: 100%;\n            height: 100%;\n            border: none;\n        }\n\n        .forecast-panel {\n            width: 350px;\n            background: linear-gradient(135deg, #dff6ff, #06283d);\n            padding: 30px;\n        }\n\n        .forecast-header {\n            margin-bottom: 20px;\n        }\n\n        .forecast-header h2 {\n            font-size: 24px;\n            font-weight: 600;\n            margin-bottom: 15px;\n        }\n\n        .search-box {\n            position: relative;\n        }\n\n        .search-box input {\n            width: 100%;\n            padding: 10px 15px;\n            padding-right: 40px;\n            background-color: rgba(255, 255, 255, 0.2);\n            border: none;\n            border-radius: 20px;\n            color: #ffffff;\n            font-size: 14px;\n        }\n\n        .search-box input::placeholder {\n            color: rgba(255, 255, 255, 0.7);\n        }\n\n        .search-box button {\n            position: absolute;\n            right: 15px;\n            top: 50%;\n            transform: translateY(-50%);\n            background: none;\n            border: none;\n            color: #ffffff;\n            cursor: pointer;\n        }\n\n        .forecast-items {\n            display: flex;\n            flex-direction: column;\n            gap: 15px;\n            margin-top: 30px;\n        }\n\n        .forecast-item {\n            background-color: rgba(223, 246, 255, 0.1);\n            border-radius: 16px;\n            padding: 15px;\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n        }\n\n        .forecast-time-container {\n            display: flex;\n            flex-direction: column;\n        }\n\n        .forecast-day {\n            font-weight: 500;\n        }\n\n        .forecast-time {\n            color: #94a3b8;\n            font-size: 14px;\n        }\n\n        .forecast-icon {\n            width: 40px;\n            height: 40px;\n            display: flex;\n            align-items: center;\n            justify-content: center;\n        }\n\n        .forecast-icon img {\n            width: 100%;\n            height: 100%;\n        }\n\n        .forecast-temp-container {\n            text-align: right;\n        }\n\n        .forecast-temp {\n            font-size: 28px;\n            font-weight: 700;\n        }\n\n        .forecast-condition {\n            color: #94a3b8;\n            font-size: 14px;\n        }\n\n        @media (max-width: 1200px) {\n            .dashboard-container {\n                flex-direction: column;\n            }\n\n            .sidebar {\n                width: 100%;\n                flex-direction: row;\n                justify-content: space-between;\n                padding: 15px;\n            }\n\n            .logo {\n                margin-bottom: 0;\n            }\n\n            .nav-items {\n                display: flex;\n            }\n\n            .nav-item {\n                margin-bottom: 0;\n                margin-right: 10px;\n            }\n\n            .main-content {\n                padding: 20px;\n            }\n\n            .forecast-panel {\n                width: 100%;\n            }\n\n            .weather-cards {\n                grid-template-columns: repeat(2, 1fr);\n            }\n        }\n\n        @media (max-width: 768px) {\n            .header {\n                flex-direction: column;\n                gap: 15px;\n            }\n\n            .station-info {\n                text-align: left;\n            }\n\n            .weather-cards {\n                grid-template-columns: 1fr;\n            }\n        }\n    </style>\n</head>\n\n<body>\n    <div class=\"dashboard-container\">\n        <!-- Sidebar -->\n        <div class=\"sidebar\">\n            <div class=\"logo\">\n                <img src=\"https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Weather%20Station%20Dashboard.jpg-hYlNXdOXcA0yAHPry60kUI7nsy6Z5h.jpeg\" alt=\"CloudNex Logo\">\n            </div>\n\n            <div class=\"nav-items\">\n                <a href=\"/dashboard\" class=\"nav-item active\">\n                    <svg class=\"nav-icon\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" fill=\"none\"\n                        stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                        <path d=\"M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\"></path>\n                        <polyline points=\"9 22 9 12 15 12 15 22\"></polyline>\n                    </svg>\n                    Dashboard\n                </a>\n\n                <a href=\"/weather-dashboard\" class=\"nav-item\">\n                    <svg class=\"nav-icon\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" fill=\"none\"\n                        stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                        <path d=\"M22 12h-4l-3 9L9 3l-3 9H2\"></path>\n                    </svg>\n                    Environmental Monitoring\n                </a>\n\n                <a href=\"/historical-chart\" class=\"nav-item\">\n                    <svg class=\"nav-icon\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" fill=\"none\"\n                        stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                        <path d=\"M3 3v18h18\"></path>\n                        <path d=\"m19 9-5 5-4-4-3 3\"></path>\n                    </svg>\n                    Historical Data\n                </a>\n            </div>\n        </div>\n\n        <!-- Main Content -->\n        <div class=\"main-content\">\n            <!-- Header -->\n            <div class=\"header\">\n                <div class=\"date-section\">\n                    <h1 id=\"current-month-year\"></h1>\n                    <p id=\"current-date\"></p>\n                </div>\n\n                <div class=\"station-info\">\n                    <h1>WEATHER STATION</h1>\n                    <p>UNIVERSITAS PRASETIYA MULYA</p>\n                </div>\n            </div>\n\n            <!-- Today Overview -->\n            <div class=\"section-header\">\n                <h2>Today Overview</h2>\n                <a href=\"/weather-dashboard\">More Detail ›</a>\n            </div>\n\n            <div class=\"weather-cards\">\n                <!-- Temperature Card -->\n                <div class=\"weather-card\">\n                    <div class=\"card-title\">\n                        <svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\"\n                            stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                            <path d=\"M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z\"></path>\n                        </svg>\n                        Temperature\n                    </div>\n                    <div class=\"card-value loading\" id=\"temperature\">-- °C</div>\n                </div>\n\n                <!-- Humidity Card -->\n                <div class=\"weather-card\">\n                    <div class=\"card-title\">\n                        <svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\"\n                            stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                            <path d=\"M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z\"></path>\n                        </svg>\n                        Humidity\n                    </div>\n                    <div class=\"card-value loading\" id=\"humidity\">-- %</div>\n                </div>\n\n                <!-- Air Particle Card -->\n                <div class=\"weather-card\">\n                    <div class=\"card-title\">\n                        <svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\"\n                            stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                            <path d=\"M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242\"></path>\n                            <path d=\"M12 12v9\"></path>\n                            <path d=\"m8 17 4 4 4-4\"></path>\n                        </svg>\n                        Air Particle\n                    </div>\n                    <div class=\"card-value loading\" id=\"airParticle\">-- μg/m³</div>\n                </div>\n\n                <!-- Wind Direction Card -->\n                <div class=\"weather-card\">\n                    <div class=\"card-title\">\n                        <svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\"\n                            stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                            <circle cx=\"12\" cy=\"12\" r=\"10\"></circle>\n                            <polygon points=\"16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76\"></polygon>\n                        </svg>\n                        Wind Direction\n                    </div>\n                    <div class=\"card-value loading\" id=\"windDirection\">--</div>\n                </div>\n\n                <!-- Wind Speed Card -->\n                <div class=\"weather-card\">\n                    <div class=\"card-title\">\n                        <svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\"\n                            stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                            <path d=\"M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2\"></path>\n                            <path d=\"M9.6 4.6A2 2 0 1 1 11 8H2\"></path>\n                            <path d=\"M12.6 19.4A2 2 0 1 0 14 16H2\"></path>\n                        </svg>\n                        Wind Speed\n                    </div>\n                    <div class=\"card-value loading\" id=\"windSpeed\">-- m/s</div>\n                </div>\n\n                <!-- Pressure Card -->\n                <div class=\"weather-card\">\n                    <div class=\"card-title\">\n                        <svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\"\n                            stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                            <path d=\"m12 14 4-4\"></path>\n                            <path d=\"M3.34 19a10 10 0 1 1 17.32 0\"></path>\n                        </svg>\n                        Pressure\n                    </div>\n                    <div class=\"card-value loading\" id=\"pressure\">-- hPa</div>\n                </div>\n            </div>\n\n            <!-- Map -->\n            <div class=\"map-container\">\n                <iframe\n                    src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3965.7798247799513!2d106.6374011!3d-6.3003877!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69fb51fc0750cf%3A0xede1a61444482883!2sUniversitas%20Prasetiya%20Mulya!5e0!3m2!1sen!2sid!4v1698765432109!5m2!1sen!2sid\"\n                    allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>\n            </div>\n        </div>\n\n        <!-- Forecast Panel -->\n        <div class=\"forecast-panel\">\n            <div class=\"forecast-header\">\n                <h2>Weather Forecast</h2>\n                <div class=\"search-box\">\n                    <input type=\"text\" id=\"locationInput\" placeholder=\"Search location here...\" onkeypress=\"if(event.key === 'Enter') debounceFetchForecast()\">\n                    <button onclick=\"debounceFetchForecast()\">\n                        <svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n                            <circle cx=\"11\" cy=\"11\" r=\"8\"></circle>\n                            <line x1=\"21\" y1=\"21\" x2=\"16.65\" y2=\"16.65\"></line>\n                        </svg>\n                    </button>\n                </div>\n            </div>\n\n            <div class=\"forecast-items\" id=\"forecastItems\">\n                <div class=\"forecast-item\">\n                    <div class=\"forecast-day\">Enter a location to see forecast...</div>\n                </div>\n            </div>\n        </div>\n    </div>\n\n    <script>\n        // --- Utility Functions ---\n        function formatValue(value, decimals = 1, unit = '', defaultValue = '--') {\n            const num = parseFloat(value);\n            if (isNaN(num) || value === null || value === undefined) {\n                return `${defaultValue} ${unit}`;\n            }\n            return `${num.toFixed(decimals)} ${unit}`;\n        }\n\n        function getWindDirectionInfo(degrees) {\n            const val = parseFloat(degrees);\n            if (isNaN(val) || val === null || val === undefined) return { code: '--', name: '--' };\n\n            const directions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest'];\n            const codes = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];\n            const index = Math.round(val / 45) % 8;\n            return {\n                code: codes[index],\n                name: directions[index]\n            };\n        }\n\n        function updateElement(id, value, isLoading = false) {\n            const element = document.getElementById(id);\n            if (!element) return;\n\n            element.classList.toggle('loading', isLoading);\n            element.textContent = isLoading ? `-- ${element.textContent.split(' ').pop()}` : value;\n        }\n\n        function updateDateTime() {\n            const now = new Date();\n            const dateOptions = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };\n            const monthYearOptions = { month: 'long', year: 'numeric' };\n\n            updateElement('current-date', now.toLocaleDateString('en-US', dateOptions));\n            updateElement('current-month-year', now.toLocaleDateString('en-US', monthYearOptions));\n        }\n\n        // --- Debounce Utility ---\n        function debounce(func, wait) {\n            let timeout;\n            return function executedFunction(...args) {\n                const later = () => {\n                    clearTimeout(timeout);\n                    func(...args);\n                };\n                clearTimeout(timeout);\n                timeout = setTimeout(later, wait);\n            };\n        }\n\n        // --- WebSocket Setup ---\n        const wsUrl = `ws://${location.hostname}:1880/ws/weather`;\n        let ws;\n        let connectionAttempts = 0;\n        const maxConnectionAttempts = 5;\n\n        function connectWebSocket() {\n            console.log(`Connecting to WebSocket (attempt ${connectionAttempts + 1})...`);\n\n            ws = new WebSocket(wsUrl);\n\n            ws.onopen = () => {\n                console.log('Connected to WebSocket');\n                connectionAttempts = 0;\n            };\n\n            ws.onmessage = (event) => {\n                try {\n                    const data = JSON.parse(event.data);\n                    console.log('Received WebSocket data:', data);\n\n                    updateElement('temperature', formatValue(data.temperature, 1, '°C'));\n                    updateElement('humidity', formatValue(data.humidity, 1, '%'));\n                    updateElement('airParticle', formatValue(data.pm25, 1, 'μg/m³'));\n                    const windDirInfo = getWindDirectionInfo(data.wind_direction);\n                    updateElement('windDirection', `${windDirInfo.code} (${windDirInfo.name})`);\n                    updateElement('windSpeed', formatValue(data.wind_speed_mps, 1, 'm/s'));\n                    updateElement('pressure', formatValue(data.pressure, 1, 'hPa'));\n                } catch (error) {\n                    console.error('Error processing WebSocket message:', error);\n                }\n            };\n\n            ws.onerror = (error) => {\n                console.error('WebSocket error:', error);\n                ws.close();\n            };\n\n            ws.onclose = () => {\n                console.log('Disconnected from WebSocket');\n                connectionAttempts++;\n\n                if (connectionAttempts < maxConnectionAttempts) {\n                    console.log(`Retrying WebSocket connection in 5 seconds... (${connectionAttempts}/${maxConnectionAttempts})`);\n                    setTimeout(connectWebSocket, 5000);\n                } else {\n                    console.error(`Failed to connect after ${maxConnectionAttempts} attempts. Using fallback data.`);\n                    useFallbackData();\n                }\n            };\n        }\n\n        function useFallbackData() {\n            const fallbackData = {\n                temperature: 29,\n                humidity: 74.9,\n                pm25: 29,\n                wind_speed_mps: 4.17,\n                wind_direction: 225,\n                pressure: 1002\n            };\n            updateElement('temperature', formatValue(fallbackData.temperature, 1, '°C'));\n            updateElement('humidity', formatValue(fallbackData.humidity, 1, '%'));\n            updateElement('airParticle', formatValue(fallbackData.pm25, 1, 'μg/m³'));\n            const windDirInfo = getWindDirectionInfo(fallbackData.wind_direction);\n            updateElement('windDirection', `${windDirInfo.code} (${windDirInfo.name})`);\n            updateElement('windSpeed', formatValue(fallbackData.wind_speed_mps, 1, 'm/s'));\n            updateElement('pressure', formatValue(fallbackData.pressure, 1, 'hPa'));\n            document.querySelectorAll('.card-value').forEach(el => {\n                el.style.color = '#7986cb';\n            });\n        }\n\n        // Initialize WebSocket\n        connectWebSocket();\n\n        // Initialize date/time display\n        updateDateTime();\n        setInterval(updateDateTime, 60000); // Update every minute\n\n        // --- Forecast Function ---\n        async function fetchForecast() {\n            const location = document.getElementById('locationInput').value || 'Universitas Prasetiya Mulya';\n            const forecastItems = document.getElementById('forecastItems');\n\n            forecastItems.innerHTML = '<div class=\"forecast-item\"><div class=\"forecast-day\">Loading forecast...</div></div>';\n\n            try {\n                const apiKey = 'efddee6b457d91e33a8e76357ffabddf';\n                const url = `https://api.openweathermap.org/data/2.5/forecast?q=${encodeURIComponent(location)}&appid=${apiKey}&units=metric`;\n                const response = await fetch(url);\n\n                if (!response.ok) {\n                    throw new Error('Location not found or API error');\n                }\n\n                const data = await response.json();\n\n                const forecastList = data.list.slice(0, 5);\n                const processedForecast = forecastList.map(item => {\n                    const date = new Date(item.dt * 1000);\n                    const day = date.toLocaleDateString('en-US', { weekday: 'long' });\n                    const time = date.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });\n                    const temp = Math.round(item.main.temp) + '°C';\n                    const condition = item.weather[0].description;\n                    const icon = `http://openweathermap.org/img/wn/${item.weather[0].icon}.png`;\n\n                    return { day, time, temp, condition, icon };\n                });\n\n                forecastItems.innerHTML = '';\n                processedForecast.forEach(item => {\n                    const forecastItem = document.createElement('div');\n                    forecastItem.className = 'forecast-item';\n                    forecastItem.innerHTML = `\n                        <div class=\"forecast-time-container\">\n                            <div class=\"forecast-day\">${item.day}</div>\n                            <div class=\"forecast-time\">${item.time}</div>\n                        </div>\n                        <div class=\"forecast-icon\">\n                            <img src=\"${item.icon}\" alt=\"Weather icon\">\n                        </div>\n                        <div class=\"forecast-temp-container\">\n                            <div class=\"forecast-temp\">${item.temp}</div>\n                            <div class=\"forecast-condition\">${item.condition}</div>\n                        </div>\n                    `;\n                    forecastItems.appendChild(forecastItem);\n                });\n            } catch (error) {\n                forecastItems.innerHTML = `<div class=\"forecast-item\">\n                    <div class=\"forecast-day\">Error: ${error.message}</div>\n                </div>`;\n            }\n        }\n\n        const debounceFetchForecast = debounce(fetchForecast, 500);\n    </script>\n</body>\n\n</html>",
        "x": 430,
        "y": 400,
        "wires": [
            [
                "cbc6bb53b15552e8"
            ]
        ]
    },
    {
        "id": "cbc6bb53b15552e8",
        "type": "http response",
        "z": "weather_dashboard_flow",
        "name": "Main Page Response",
        "statusCode": "200",
        "headers": {
            "Content-Type": "text/html"
        },
        "x": 720,
        "y": 400,
        "wires": []
    },
    {
        "id": "1498bfb91f583e3e",
        "type": "mqtt-broker",
        "name": "Server",
        "broker": "10.10.169.249",
        "port": 1883,
        "clientid": "",
        "autoConnect": true,
        "usetls": false,
        "protocolVersion": 4,
        "keepalive": 60,
        "cleansession": true,
        "autoUnsubscribe": true,
        "birthTopic": "",
        "birthQos": "0",
        "birthRetain": "false",
        "birthPayload": "",
        "birthMsg": {},
        "closeTopic": "",
        "closeQos": "0",
        "closeRetain": "false",
        "closePayload": "",
        "closeMsg": {},
        "willTopic": "",
        "willQos": "0",
        "willRetain": "false",
        "willPayload": "",
        "willMsg": {},
        "userProps": "",
        "sessionExpiry": ""
    },
    {
        "id": "7e3e0898da3593ac",
        "type": "websocket-listener",
        "path": "/ws/weather",
        "wholemsg": "true"
    }
]
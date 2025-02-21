from textwrap import dedent
from jinja2 import Template

FRONTEND_TEMPLATE = Template(
    dedent("""
        <html>
            <head>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-100 min-h-screen p-8">
                <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
                    <h1 class="text-3xl font-bold text-gray-800 mb-6">Session Information - <a class="text-blue-500" href="https://webgenieai.co/">WebgeneiAI</a></h1>
                    <div class="space-y-4">
                        <p class="text-gray-700">
                            <span class="font-semibold">Available Competitions:</span> 
                            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded">{{ available_competitions }}</span>
                        </p>
                        <p class="text-gray-700">
                            <span class="font-semibold">Session:</span>
                            <span class="ml-2">{{ info['session'] }}</span>
                        </p>
                        <p class="text-gray-700">
                            <span class="font-semibold">Current Competition:</span>
                            <span class="ml-2">{{ info['current_competition'] }}</span>
                        </p>
                        <p class="text-gray-700">
                            <span class="font-semibold">Current Time:</span>
                            <span class="ml-2">{{ info['current_datetime'] }}</span>
                        </p>
                        <p class="text-gray-700">
                            <span class="font-semibold">Session Start:</span>
                            <span class="ml-2">{{ info['session_start_datetime'] }}</span>
                        </p>
                        <p class="text-gray-700">
                            <span class="font-semibold">Session End:</span>
                            <span class="ml-2">{{ info['session_end_datetime'] }}</span>
                        </p>
                    </div>
                </div>
                <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
                    <h1 class="text-3xl font-bold text-gray-800 mb-6">Go to Url And Get Related Uids</h1>
                    <div class="space-y-4">
                        <p class="text-gray-700">
                            http://209.126.9.130:8007/related_uids?subnet_uid=54&uid=134
                        </p>    
                    </div>
                </div>
            </body>
        </html>
    """
    )
)
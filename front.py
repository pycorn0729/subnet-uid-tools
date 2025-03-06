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
                <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6 mt-6">
                    <h1 class="text-3xl font-bold text-gray-800 mb-6">Related UIDs</h1>
                    <div class="space-y-4">
                        <p class="text-gray-700">
                            <span class="font-semibold">Related UIDs:</span>
                            <a href="/related_uids?subnet_uid=54&uid=9" class="text-blue-500 hover:text-blue-700 ml-2"> Get Related UIDs </a>
                        </p>
                    </div>
                </div>
                
                <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6 mt-6">
                    <h1 class="text-3xl font-bold text-gray-800 mb-6">Code Repository</h1>
                    <div class="space-y-4">
                        <p class="text-gray-700">
                            <span class="font-semibold">GitHub Repository:</span>
                            <a href="https://github.com/pycorn0729/subnet-uid-tools.git" class="text-blue-500 hover:text-blue-700 ml-2">
                                https://github.com/pycorn0729/subnet-uid-tools.git
                            </a>
                        </p>
                        <p class="text-gray-600 text-sm mt-2">
                            Visit the repository for source code and documentation.
                        </p>
                    </div>
                </div>
            </body>
        </html>
    """
    )
)
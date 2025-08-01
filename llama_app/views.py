from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import subprocess
import json

@csrf_exempt
def llama_inference(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            cmd = [
                "/home/jonathan/llama.cpp/build/bin/llama-cli",
                "-m", "/home/jonathan/llama.cpp/models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf",
                "-n", "128",
                "-c", "2048"
            ]

            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60
            )

            print("LLAMA returncode:", result.returncode)
            print("LLAMA stdout:", result.stdout)
            print("LLAMA stderr:", result.stderr)

            if result.returncode != 0:
                return JsonResponse({"error": result.stderr}, status=500)

            return JsonResponse({"response": result.stdout})

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

from fastapi import FastAPI, HTTPException
import openai
import requests

app = FastAPI()

# Set your OpenAI API key
api_key = "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"

@app.post("/generate_recipe")
async def generate_recipe(ingredients: list):
    # Check if ingredients are provided
    if not ingredients:
        raise HTTPException(status_code=400, detail="Please provide a list of ingredients")

    # Generate recipe using OpenAI's API
    prompt = "Generate a recipe using the following ingredients: " + ", ".join(ingredients)
    try:
        # Define parameters
        params = {
            "prompt": prompt,
            "max_tokens": 200
        }

        # Make a POST request to the OpenAI API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        print(prompt)

        response = requests.post("https://api.openai.com/v1/completions", json=params, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Get the generated text from the response
            recipe = response.json()["choices"][0]["text"].strip()
            return {"recipe": recipe}
        else:
            raise HTTPException(status_code=500, detail="Failed to generate recipe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
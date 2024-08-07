from fastapi import FastAPI, HTTPException
import requests
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware


#RecipeRadar --Author Siddhi Kotre--
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Set your OpenAI API key
api_key = "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"

@app.post("/generate_recipe")
async def generate_recipe(ingredients: str):
    print(ingredients)
    # Check if ingredients are provided
    if not ingredients:
        raise HTTPException(status_code=400, detail="Please provide a list of ingredients")
    
    # Generate recipe using OpenAI's API
    prompt = "Generate a recipe using the following ingredients(recipe):" + ", ".join(ingredients)
    try:
        client = OpenAI(api_key = api_key)
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo", 
            messages = [
                {
                    "role" : "user",
                    "content" : prompt
                },
            ],
        )
        
        # Get the generated text from the responses and displaying it
        recipe = response.choices[0].message.content
        return {"Recipe" : recipe}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

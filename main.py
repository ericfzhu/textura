from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
from collections import Counter
import stability

app = FastAPI()


class GenerateArtRequest(BaseModel):
    prompt: str


class ArtPalette(BaseModel):
    colors: List[List[float]]


@app.post("/generate_art")
async def generate_art(request: GenerateArtRequest):
    # Generate the art
    prompt = request.prompt
    image = stability.generate_image(prompt)

    # Get the color palette
    palette = extract_palette(image)

    # Filter and return the color palette
    filtered_palette = filter_palette(palette, 5)
    response = {
        "colors": filtered_palette
    }

    return JSONResponse(content=response)


def extract_palette(image):
    '''Opens an image file and retrieves its palette.'''
    try:
        palette = image.getpalette()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not retrieve image palette: {e}")
    return palette


def filter_palette(palette, num_colors):
    '''Filters the color palette to return the most prominent colors.'''
    # Convert the color palette to a list
    palette_list = np.array(palette).reshape(-1, 3).tolist()

    # Count the number of occurrences of each color
    color_counts = Counter(tuple(item) for item in palette_list)

    # Get the most common colors
    most_common_colors = color_counts.most_common(num_colors)

    # Convert RGB tuples back to ints
    filtered_palette = [item[0] for item in most_common_colors]

    return filtered_palette


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
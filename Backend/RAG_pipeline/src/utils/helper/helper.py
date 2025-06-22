import json
import re
import textwrap
async def get_json_response(response):
    match = re.search(r'\{.*\}',response,re.DOTALL)
    if match:
        json_text=match.group(0)
        try:
            result=json.loads(json_text)
            return result
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
    else:
        print("No valid JSON found in the response")
    return None

async def get_pagewise_txt(doc):
    """
    This function is responsible for making seprating the pages from a txt doc , who do not have pdfs mentioned properly in their txt.
    """
    pass


#!/usr/bin/env python3
"""
generate_testdata.py
-----------------------------------
Generate a Django loaddata fixture of synthetic papers using OpenAI's structured output
to ensure consistent, valid data format.

Usage:
    export OPENAI_API_KEY="sk-..."  # Standard OpenAI env var name
    pip install openai
    python generate_testdata.py
"""

import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any

from openai import OpenAI

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
MODEL_NAME = "gpt-4o"
TOTAL = 200              # total records desired
BATCH_SIZE = 5           # papers per API request
TEMPERATURE = 0.8
OUTPUT_FILE = "../backend/papers/fixtures/papers.json"

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("MV_OPENAI_KEY"))
if not client.api_key:
    raise RuntimeError("MV_OPENAI_KEY environment variable not set")

# ---------------------------------------------------------------------
# SCHEMA DEFINITION
# ---------------------------------------------------------------------
PAPER_SCHEMA = {
    "type": "object",
    "properties": {
        "papers": {
            "type": "array",
            "description": "List of paper objects for a Django fixture",
            "items": {
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "enum": ["papers.paper"],
                        "description": "Django model name"
                    },
                    "pk": {
                        "type": "integer",
                        "description": "Primary key, should increment from the starting value"
                    },
                    "fields": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the scientific paper"
                            },
                            "authors": {
                                "type": "string",
                                "description": "Comma-separated list of fictional authors (first name, last name)"
                            },
                            "journal": {
                                "type": "string",
                                "description": "Name of a fictional scientific journal"
                            },
                            "invivo_model": {
                                "type": "string",
                                "description": "Type of in-vivo model used (e.g., formalin pain model, Morris water maze)"
                            },
                            "abstract": {
                                "type": "string",
                                "description": "Scientific abstract of the paper in 6-7 sentences"
                            },
                            "condition_sets": {
                                "type": "array",
                                "description": "Array of condition objects describing experimental conditions",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "description": "Type of condition (e.g., species, age, gender, dose)"
                                        },
                                        "value": {
                                            "type": "string",
                                            "description": "Value of the condition"
                                        }
                                    },
                                    "required": ["type", "value"]
                                }
                            },
                            "is_important": {
                                "type": "boolean",
                                "description": "Whether this paper is marked as important",
                                "default": False
                            }
                        },
                        "required": ["title", "authors", "journal", "invivo_model", "abstract", "condition_sets", "is_important"]
                    }
                },
                "required": ["model", "pk", "fields"]
            }
        }
    },
    "required": ["papers"]
}

# ---------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------
def generate_batch(num: int, start_pk: int) -> List[Dict[str, Any]]:
    """Generate a batch of paper records using OpenAI's structured output."""
    
    system_prompt = (
        "You are a data generator for a biotechnology startup's test database. "
        "Generate realistic but fictional scientific papers focused on in-vivo experiments. "
        "Each paper should have varied in-vivo models (e.g., formalin pain model, Morris water maze, xenograft). "
        "Use fictional authors and journals. Make sure condition_sets include animal species, strain, age, and other "
        "relevant experimental parameters."
    )
    
    user_prompt = f"Generate {num} synthetic paper records starting at primary key {start_pk}. Respond in JSON format."
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        tools=[{
            "type": "function",
            "function": {
                "name": "generate_papers",
                "description": "Generate a batch of scientific paper records",
                "parameters": PAPER_SCHEMA
            }
        }],
        tool_choice={"type": "function", "function": {"name": "generate_papers"}}
    )
    
    # Extract the generated papers from the tool call
    tool_call = response.choices[0].message.tool_calls[0]
    papers_data = json.loads(tool_call.function.arguments)
    
    return papers_data["papers"]

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def main():
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    batches_needed = (TOTAL + BATCH_SIZE - 1) // BATCH_SIZE
    print(
        f"Generating {TOTAL} papers in {batches_needed} batches "
        f"({BATCH_SIZE} per call) with model {MODEL_NAME} …"
    )

    all_papers = []
    current_pk = 1

    for batch_idx in range(batches_needed):
        batch_size = min(BATCH_SIZE, TOTAL - len(all_papers))
        print(f" • Batch {batch_idx+1}/{batches_needed} (PK {current_pk}–{current_pk+batch_size-1})", end=" ")
        
        try:
            papers = generate_batch(batch_size, current_pk)
            all_papers.extend(papers)
            current_pk += batch_size
            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")
            # Continue with next batch
        
        # Small delay to avoid rate limits
        time.sleep(1)

    # Write to output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fp:
        json.dump(all_papers, fp, indent=2)
    
    print(f"\n🎉 Generated {len(all_papers)} papers")
    print(f"📄 Saved fixture to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

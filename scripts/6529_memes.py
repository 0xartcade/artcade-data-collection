import httpx
from dotenv import load_dotenv
import json
import os

load_dotenv()

"""
User inputs
"""
start_token = 1
end_token = 302

"""
Script (DO NOT MODIFY BELOW)
"""
with httpx.Client(
    base_url="https://api.simplehash.com/api/v0/nfts/ethereum/0x33fd426905f149f8376e227d0c9d3340aad17af1"
) as client:
    raw_data = []
    for token_id in range(start_token, end_token + 1):
        print(f"Collecting info for token id {token_id}")
        r = client.get(
            f"/{token_id}",
            headers={
                "X-API-KEY": os.environ.get("SIMPLEHASH_API_KEY"),
                "accept": "application/json",
            },
        )

        if r.status_code != 200:
            raise Exception(f"Failed response: {r.text}")

        data = r.json()

        raw_data.append(
            {
                "collection": "The Memes by 6529",
                "contract_address": "0x33fd426905f149f8376e227d0c9d3340aad17af1",
                "token_id": token_id,
                "questions": {
                    "title": data["name"],
                    "artist": next(
                        (
                            item["value"]
                            for item in data["extra_metadata"]["attributes"]
                            if item["trait_type"].lower() == "artist"
                        ),
                        None,
                    ),
                    "supply": data["token_count"],
                    "season": next(
                        (
                            item["value"]
                            for item in data["extra_metadata"]["attributes"]
                            if item["trait_type"].lower() == "type - season"
                        ),
                        None,
                    ),
                },
                "image_url": data["previews"]["image_medium_url"],
                "blurhash": data["previews"]["blurhash"],
                "predominant_color": data["previews"]["predominant_color"],
            }
        )

# gathered the data, now create some entries for gather fake question answers
print("Running analytics")
title_list = list(set([item["questions"]["title"] for item in raw_data]))
supply_list = list(set([item["questions"]["supply"] for item in raw_data]))
artist_list = list(set([item["questions"]["artist"] for item in raw_data]))
season_list = list(set([item["questions"]["season"] for item in raw_data]))

# combine all this data
output = {
    "raw_data": raw_data,
    "titles": title_list,
    "supplies": supply_list,
    "artists": artist_list,
    "seasons": season_list,
}

# output the data
with open(f"outputs/6529-memes-{start_token}-{end_token}.json", "w") as out:
    json.dump(output, out, indent=4)

print("Success!")

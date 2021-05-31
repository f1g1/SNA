import json

with open("final-formatted.json", "rb") as f:
    jsonData = json.load(f)

for i in range(0, len(jsonData)):
    if(jsonData[i]["Genre"] is None):
        continue

    movie_genres = [z.strip() for z in jsonData[i]["Genre"].split(",")]

    jsonData[i]["RelatedMovieByGenre"] = []
    for j in range(1, len(jsonData) - 1):
        for genre in movie_genres:
            if(jsonData[j]["Genre"] is not None and jsonData[j]["Genre"].find(genre) != -1):
                jsonData[i]["RelatedMovieByGenre"].append((jsonData[j]["Id"],genre))

with open("repr2-data.json", "w") as f:
    json.dump(jsonData, f)
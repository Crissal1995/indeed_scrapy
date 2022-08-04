import datetime
import os
import pprint
import string
from typing import Any, List, Optional

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


def get_or_raise(key: str, default: Optional[Any] = None) -> Any:
    value = os.getenv(key)
    if value is None:
        if default:
            return default
        else:
            raise EnvironmentError(f"Missing key: {key}")
    return value


def to_camel(string: str) -> str:
    return "".join(
        word if i == 0 else word.capitalize()
        for i, word in enumerate(string.split("_"))
    )


class ToSnakeCaseModel(BaseModel):
    class Config:
        alias_generator = to_camel


class Status(ToSnakeCaseModel):
    id: str
    name: str
    canonical_name: str


class Candidate(ToSnakeCaseModel):
    candidate_id: str
    job_id: str
    name: str
    location: str
    status_id: str


class JobInfo(ToSnakeCaseModel):
    job_id: str
    title: str
    status: str


class Response(ToSnakeCaseModel):
    candidates: List[Candidate]
    job_info: List[JobInfo]
    statuses: List[Status]


headers = {
    "authority": "employers.indeed.com",
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "cookie": get_or_raise("COOKIE"),
    "dnt": "1",
    "indeed-client-application": "entcand",
    "pragma": "no-cache",
    "referer": "https://employers.indeed.com/c",
    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": get_or_raise("USER_AGENT"),
    "x-datadog-origin": "rum",
    "x-datadog-parent-id": get_or_raise("DATADOG_PARENT_ID"),
    "x-datadog-sampled": "1",
    "x-datadog-sampling-priority": "1",
    "x-datadog-trace-id": get_or_raise("DATADOG_TRACE_ID"),
    "x-indeed-api": "1",
    "x-indeed-appname": "entcand",
    "x-indeed-apptype": "desktop",
    "x-indeed-rpc": "1",
    "x-indeed-tk": get_or_raise("INDEED_TOKEN"),
}

base_url = "https://employers.indeed.com/api/ctws/preview/candidates?offset=$offset&encryptedJobId=0"

OUTPUT_FILE = "responses.txt"
NOW = datetime.datetime.now()

with open(OUTPUT_FILE, "a") as f:
    f.write(f"{NOW}\n")


more_candidates = True
offset = 0
i = 0

while more_candidates:
    url = string.Template(base_url).substitute(offset=offset)

    r = requests.get(url, headers=headers)
    data = r.json()
    response = Response(**data)

    # pprint.pp(response.candidates)
    num_candidates = len(response.candidates)
    print(f"Found {num_candidates} candidates [round {i+1}]")

    with open(OUTPUT_FILE, "a") as f:
        pprint.pp(response.json(), f)

    offset += num_candidates
    more_candidates = num_candidates > 0

print(f"Stored {offset} candidates")

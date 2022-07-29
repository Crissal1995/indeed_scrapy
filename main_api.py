import os
import pprint
from typing import List

import requests
from pydantic import BaseModel


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


headers = {
    "authority": "employers.indeed.com",
    "accept": "application/json",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "cookie": os.getenv("COOKIE"),
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
    "user-agent": os.getenv("USER_AGENT"),
    "x-datadog-origin": "rum",
    "x-datadog-parent-id": os.getenv("DATADOG_PARENT_ID"),
    "x-datadog-sampled": "1",
    "x-datadog-sampling-priority": "1",
    "x-datadog-trace-id": os.getenv("DATADOG_TRACE_ID"),
    "x-indeed-api": "1",
    "x-indeed-appname": "entcand",
    "x-indeed-apptype": "desktop",
    "x-indeed-rpc": "1",
    "x-indeed-tk": os.getenv("INDEED_TOKEN"),
}

url = (
    "https://employers.indeed.com/api/ctws/preview/candidates?offset=0&encryptedJobId=0"
)

r = requests.get(url, headers=headers)
response = Response(**r.json())

pprint.pp(response.candidates)
print(f"Found {len(response.candidates)} candidates")

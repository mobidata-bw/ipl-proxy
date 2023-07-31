"""
MobiData BW Proxy
Copyright (c) 2023, binary butterfly GmbH
All rights reserved.
"""

from abc import ABC, abstractmethod
from typing import Union, List

from mitmproxy.http import HTTPFlow


class BaseConverter(ABC):
    @property
    @abstractmethod
    def hostnames(self) -> List[str]:
        return []

    @abstractmethod
    def convert(self, data: Union[dict, list], path: str, flow: HTTPFlow) -> Union[dict, list]:
        pass

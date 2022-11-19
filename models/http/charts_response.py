from dataclasses import dataclass

from models.database.chart import Chart
from models.http.response_model import ResponseModel

@dataclass
class ChartsResponse(ResponseModel):
    id: int
    type: str
    title: str
    subtitle: str

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'type': self.type,
        }

    @classmethod
    def from_chart(cls, chart: Chart):
        return cls(chart.id, chart.type, chart.title, chart.subtitle)

class Chart:
    def __init__(self, chart_title: str, chart_data: str):
        self.chart_tite = chart_title
        self.chart_data = chart_data

    def to_dict(self):
        return {
            "chart_title": chart_title,
            "chart_data": chart_data,
        }

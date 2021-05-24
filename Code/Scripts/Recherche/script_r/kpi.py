import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP, "assets/style.css"]


def card(name, desc, value, color):
 
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.P(
                            html.Img(
                                src=f"https://thispersondoesnotexist.com/image",
                                className="card-img",
                            )
                        ),
                        html.H4(name, className="card-title"),
                        html.P(desc, className="card-desc"),
                        html.P(f"{value:,}", className="card-text"),
                        html.P("Key Metric", className="card-kpi"),
                        html.P("Last 15 minutes", className="card-bottom"),
                    ],
                    className="text-center mx-auto",
                )
            ],
            style={
                "background": f"linear-gradient(to bottom, {color} 25%, #FFFFFF 0%)"
            },
        ),
        className="col-auto mb-3",
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container(
    html.Div(
        [
            html.H1("Card Component", className="text-center"),
            dbc.Row(
                [
                    card(f"John Doe", "Business Owner", 2, "green"),
                    card(f"Jane Doe", "Millionaire", 103, "blue"),
                    card(f"Juan Alimaña", "Entrepreneur", 104, "red"),
                ],
                className="cards justify-content-center",
            ),
        ]
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)

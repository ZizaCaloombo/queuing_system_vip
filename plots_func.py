def draw_plot(title, x_title, y_title, file_name="plot.html", **plot_data):
    """
    Simple wrapper function for drawing graphs in Plotly
    -------IMPORTANT!!!!!!------
    plot_data has dict type with necessary param - x_axis
    -------IMPORTANT!!!!!!------
    :param title: graph title
    :param x_title: title of x axis
    :param y_title: title of y axis
    :param file_name: file name with its type
    :param plot_data: data for graph type: dict(x_axis=some_data). Default dict's param is x_axis and its IMPORTANT!!!!!
    :return:
    """

    import plotly
    import plotly.graph_objs as go

    if "x_axis" not in plot_data or not plot_data["x_axis"]:
        raise KeyError("Dictionary haven't '{0}' key or '{0}' have unexpected value".format("x_axis"))
    if "x_type" not in plot_data or not plot_data["x_type"]:
        plot_data["x_type"] = "scatter"
    if "y_type" not in plot_data or not plot_data["y_type"]:
        plot_data["y_type"] = "scatter"

    data = [go.Scatter(x=plot_data["x_axis"], y=plot_data[name], name=name)
            for name in plot_data if name not in ["x_axis", "x_type", "y_type"]
            ]

    layout = go.Layout(title=u"{}".format(title),
                       xaxis=dict(title=u"{}".format(x_title), type="{}".format(plot_data["x_type"])),
                       yaxis=dict(title=u"{}".format(y_title), type="{}".format(plot_data["y_type"])),
                       )

    plot = dict(data=data, layout=layout)
    plotly.offline.plot(plot, filename=file_name)
import plotly.graph_objects as go


labels=['Ajustes', 'Gasolina', 'Reparacion y mantenimiento', 'Obras beneficas', 'Ropa', 'Informatica', 'Educacion', 'Multimedia', 'Viajes', 'Social', 'Regalos', 'Comida & casa', 'Hobbies', 'Seguros', 'Gastos medicos', 'Otros gastos', 'Servicios Internet', 'Telefono', 'Transporte publico', 'Suscripciones', 'Material de oficina', 'Impuestos', 'Servicios', 'Deporte', 'Medicina y vision', 'Estetica']
parents=['Gastos', 'Automovil', 'Automovil', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Ocio', 'Ocio', 'Ocio', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos', 'Gastos']
values=[0.0, 40.0, 66.35, 17.4, 79.36, 0.0, 9.75, 71.6, 327.12, 346.39, 0.0, 457.25, 0.0, -47.38, 10.0, 19.01, 0.0, 0.0, 4.8, 0.0, 0.0, 0.0, 0.0, 174.64, 92.5, 11.0]

# labels=["Cain", "Seth"]
# parents=["Eve", "Eve"]
# values=[14, 12]

# labels=["Ajustes", "Gasolina", "Automovil"]
# parents=["Gastos", "Automovil", "Gastos"]
# values=[14, 12, 10]

fig =go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

fig.write_image("fig1.png")
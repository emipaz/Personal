def plantilla_receta_html(
    titulo, 
    descripcion,
    ingredientes,
    pasos,
    img_principal, 
    img_ingredientes, 
    img_pasos, 
):
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{titulo}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            background: url('/static/recetas/img/fondo.jpg') no-repeat center center fixed;
            background-size: cover;
            color: #333;
        }}
        .container {{
            background: rgba(255,255,255,0.50);
            max-width: 900px;
            margin: 40px auto;
            border-radius: 18px;
            box-shadow: 0 8px 32px rgba(44,62,80,0.18);
            padding: 32px;
        }}
        .titulo {{
            text-align: center;
            font-size: 2.8em;
            font-weight: bold;
            color: #fff;
            margin-bottom: 18px;
            letter-spacing: 2px;
            background: linear-gradient(90deg, #8e44ad 60%, #6c3483 100%);
            border-radius: 12px;
            padding: 16px 0;
            box-shadow: 0 2px 8px rgba(142,68,173,0.18);
        }}
        .violeta-box {{
            background: linear-gradient(135deg, #8e44ad 80%, #6c3483 100%);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 32px;
            color: #fff;
            box-shadow: 0 4px 16px rgba(142,68,173,0.12);
        }}
        .descripcion-img {{
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 32px;
            margin-bottom: 28px;
            justify-content: space-between;
        }}
        .img-principal {{
            width: 340px;
            height: 340px;
            object-fit: cover;
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(46,139,87,0.18);
            margin-bottom: 0;
            margin-left: 48px;
            margin-right: 0;
            align-self: center;
        }}
        .descripcion {{
            display: flex;
            font-size: 1.3em;
            color: #fff;
            text-align: left;
            max-width: 75%;
            flex: 1;
        }}
        .ingredientes-section {{
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 32px;
            margin-bottom: 28px;
            justify-content: flex-start;
        }}
        .img-ingredientes {{
           width: 260px;
            height: 260px;
            object-fit: cover;
            border-radius: 18px;
            box-shadow: 0 4px 16px rgba(52,152,219,0.15);
            margin-bottom: 0;
            margin-right: 48px;
            margin-left: 0;
            align-self: center;
        }}
        .ingredientes-list {{
            max-width: 75%;
            flex: 1;
        }}

        .ingredientes-list h2 {{
            color: #ffe066;
            text-align: center;
            margin-bottom: 10px;
        }}

        .ingredientes-list ul {{
            font-size: 1.2em;
            padding-left: 0;
            color: #fff;
            list-style: disc inside;
            text-align: left;
        }}
        .pasos-section {{
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 24px;
            justify-content: flex-start;
        }}
        .img-pasos {{
            width: 260px;
            height: 260px;
            object-fit: cover;
            border-radius: 18px;
            box-shadow: 0 4px 16px rgba(155,89,182,0.15);
            margin-bottom: 0;
            margin-left: 100px;
            margin-right: 0;
            align-self: center;
        }}
        .pasos-list {{
            max-width: 75%;
            flex: 1;
        }}
        .pasos-list h2 {{
            color: #ffe066;
            text-align: center;
            margin-bottom: 10px;
        }}
        .pasos-list ol {{
            font-size: 1.2em;
            padding-left: 0;
            color: #fff;
            list-style: decimal inside;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="titulo">{titulo}</div>
        <div class="violeta-box descripcion-img">
            <div class="descripcion">{descripcion}</div>
            <img src="{img_principal}" alt="Receta" class="img-principal">
        </div>
        <div class="violeta-box ingredientes-section">
            <img src="{img_ingredientes}" alt="Ingredientes" class="img-ingredientes">
            <div class="ingredientes-list">
                <h2>Ingredientes</h2>
                <ul>
                    {''.join(f'<li>{ing}</li>' for ing in ingredientes)}
                </ul>
            </div>
        </div>
        <div class="violeta-box pasos-section">
            <div class="pasos-list">
                <h2>Pasos</h2>
                <oçul>
                    {''.join(f'<li>{paso}</li>' for paso in pasos)}
                </ul>
            </div>
            <img src="{img_pasos}" alt="Pasos" class="img-pasos">
        </div>
    </div>
</body>
</html>
"""
from PIL import Image
import colorsys

def rgb_to_hex(rgb):
    """Convierte RGB a hexadecimal"""
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_color_palette(image_path):
    """Extrae una paleta de colores simple"""
    try:
        # Abrir imagen
        image = Image.open(image_path)
        image = image.convert('RGB')
        
        # Redimensionar
        image = image.resize((50, 50))
        
        # Obtener todos los colores únicos
        colors = image.getcolors(maxcolors=256*256*256)
        
        if not colors:
            return None
            
        # Ordenar por frecuencia
        colors.sort(reverse=True, key=lambda x: x[0])
        
        # Filtrar colores útiles (no muy claros ni grises)
        useful_colors = []
        for count, (r, g, b) in colors:
            # Calcular luminancia
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            
            # Calcular saturación simple
            max_rgb = max(r, g, b)
            min_rgb = min(r, g, b)
            saturation = (max_rgb - min_rgb) / max_rgb if max_rgb > 0 else 0
            
            # Filtrar colores muy claros o muy grises
            if luminance < 0.9 and saturation > 0.05 and count > 10:
                useful_colors.append((count, (r, g, b)))
                
        return useful_colors[:10]  # Top 10 colores útiles
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def suggest_navbar_colors(colors):
    """Sugiere colores para la navbar basado en los colores del logo"""
    if not colors:
        return
        
    print("\n🎨 COLORES ENCONTRADOS EN EL LOGO:")
    print("=" * 60)
    
    for i, (count, (r, g, b)) in enumerate(colors[:5]):
        hex_color = rgb_to_hex([r, g, b])
        percentage = (count / sum([c for c, _ in colors])) * 100
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        brightness = "claro" if luminance > 0.5 else "oscuro"
        
        print(f"{i+1}. {hex_color} - RGB({r}, {g}, {b}) - {brightness} ({percentage:.1f}%)")
    
    print("\n🚀 SUGERENCIAS PARA LA NAVBAR:")
    print("=" * 60)
    
    # Tomar los 3 colores más dominantes
    top_colors = colors[:3]
    
    for i, (_, (r, g, b)) in enumerate(top_colors):
        original_hex = rgb_to_hex([r, g, b])
        
        # Convertir a HSV
        r_norm, g_norm, b_norm = r/255, g/255, b/255
        h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
        
        # Crear versión más oscura para navbar
        dark_v = max(v * 0.6, 0.2)
        dark_s = min(s * 1.2, 1.0)
        dark_r, dark_g, dark_b = colorsys.hsv_to_rgb(h, dark_s, dark_v)
        dark_hex = rgb_to_hex([dark_r*255, dark_g*255, dark_b*255])
        
        # Crear versión aún más oscura para gradiente
        darker_v = max(v * 0.35, 0.1)
        darker_r, darker_g, darker_b = colorsys.hsv_to_rgb(h, dark_s, darker_v)
        darker_hex = rgb_to_hex([darker_r*255, darker_g*255, darker_b*255])
        
        print(f"\nOpción {i+1} (basada en {original_hex}):")
        print(f"  • Color principal: {dark_hex}")
        print(f"  • Gradiente sugerido: linear-gradient(135deg, {dark_hex}, {darker_hex})")

def main():
    logo_path = "static/img/logo.jpg"
    
    print("🔍 ANALIZANDO COLORES DEL LOGO...")
    colors = get_color_palette(logo_path)
    
    if colors:
        suggest_navbar_colors(colors)
        
        # Generar código CSS sugerido
        if colors:
            _, (r, g, b) = colors[0]  # Color más dominante
            r_norm, g_norm, b_norm = r/255, g/255, b/255
            h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
            
            # Crear colores para navbar
            dark_v = max(v * 0.6, 0.2)
            dark_s = min(s * 1.2, 1.0)
            dark_r, dark_g, dark_b = colorsys.hsv_to_rgb(h, dark_s, dark_v)
            main_color = rgb_to_hex([dark_r*255, dark_g*255, dark_b*255])
            
            darker_v = max(v * 0.35, 0.1)
            darker_r, darker_g, darker_b = colorsys.hsv_to_rgb(h, dark_s, darker_v)
            secondary_color = rgb_to_hex([darker_r*255, darker_g*255, darker_b*255])
            
            print(f"\n💻 CÓDIGO CSS SUGERIDO:")
            print("=" * 60)
            print(f"""
/* Reemplaza 'bg-primary' en el HTML con 'navbar-custom' */
.navbar-custom {{
    background: linear-gradient(135deg, {main_color}, {secondary_color});
    box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}}

.navbar-custom .navbar-brand,
.navbar-custom .nav-link {{
    color: white !important;
}}

.navbar-custom .nav-link:hover {{
    color: rgba(255,255,255,0.8) !important;
}}
""")
    else:
        print("No se pudieron extraer colores del logo.")

if __name__ == "__main__":
    main()
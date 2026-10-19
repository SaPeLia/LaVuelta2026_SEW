import xml.etree.ElementTree as ET
from html import escape
import math


class Xml2Altimetria:
    """Genera el perfil altimétrico SVG a partir de etapaEsquema.xml."""

    def __init__(self, archivo_xml):
        self.arbol = ET.parse(archivo_xml)
        self.raiz = self.arbol.getroot()
        self.ns = {"u": "http://www.uniovi.es"}

        self.ancho = 1200
        self.alto = 620
        self.margen_izquierdo = 90
        self.margen_derecho = 35
        self.margen_superior = 55
        self.margen_inferior = 105

    def obtener_datos(self):
        """Extrae por XPath los puntos y los devuelve ordenados por distancia."""
        datos = []

        # XPath: punto de salida (distancia 0 km).
        salida = self.raiz.find("./u:ciudadSalida/u:puntoGeografico", self.ns)
        if salida is not None:
            nombre_salida = self.raiz.find("./u:ciudadSalida", self.ns).get("nombre", "Salida")
            datos.append((0.0, self.obtener_altitud(salida), nombre_salida))

        # XPath obligatorio: puntos anónimos y sus distancias/altitudes.
        for punto in self.raiz.findall("./u:puntosAnónimos/u:puntoAnónimo", self.ns):
            distancia_elemento = punto.find("./u:distanciaDesdeSalida", self.ns)
            geografico = punto.find("./u:puntoGeografico", self.ns)
            if distancia_elemento is not None and geografico is not None:
                distancia = float(distancia_elemento.text.strip().replace(",", "."))
                altitud = self.obtener_altitud(geografico)
                nombre = punto.get("nombre", "Punto")
                datos.append((distancia, altitud, nombre))

        # XPath obligatorio: hitos (puertos y sprints).
        for hito in self.raiz.findall("./u:hitos/u:hito", self.ns):
            distancia_elemento = hito.find("./u:distanciaDesdeSalida", self.ns)
            geografico = hito.find("./u:puntoGeografico", self.ns)
            if distancia_elemento is not None and geografico is not None:
                distancia = float(distancia_elemento.text.strip().replace(",", "."))
                altitud = self.obtener_altitud(geografico)
                elemento_hito = hito.find("./u:puerto", self.ns)
                if elemento_hito is None:
                    elemento_hito = hito.find("./u:sprint", self.ns)
                nombre = "Hito"
                if elemento_hito is not None:
                    nombre = elemento_hito.get("nombre", elemento_hito.get("tipo", "Hito"))
                datos.append((distancia, altitud, nombre))

        # XPath: longitud total y punto de llegada.
        longitud_elemento = self.raiz.find("./u:longitud", self.ns)
        llegada = self.raiz.find("./u:ciudadLlegada/u:puntoGeografico", self.ns)
        if longitud_elemento is not None and llegada is not None:
            distancia_final = float(longitud_elemento.text.strip().replace(",", "."))
            nombre_llegada = self.raiz.find("./u:ciudadLlegada", self.ns).get("nombre", "Llegada")
            datos.append((distancia_final, self.obtener_altitud(llegada), nombre_llegada))

        # Ordenar por distancia para dibujar el perfil de izquierda a derecha.
        datos.sort(key=lambda dato: dato[0])

        # Mantener puntos que coincidan en distancia: pueden representar un hito
        # cuya altitud difiere del punto anónimo registrado en esa misma distancia.
        if len(datos) < 2:
            raise ValueError("No hay suficientes puntos con distancia y altitud para dibujar el perfil.")
        return datos

    def obtener_altitud(self, punto_geografico):
        """Obtiene la altitud mediante XPath."""
        elemento = punto_geografico.find("./u:altitud", self.ns)
        if elemento is None or elemento.text is None:
            raise ValueError("Un puntoGeografico no contiene altitud.")
        return float(elemento.text.strip().replace(",", "."))

    def convertir_x(self, distancia, distancia_maxima):
        ancho_util = self.ancho - self.margen_izquierdo - self.margen_derecho
        return self.margen_izquierdo + (distancia / distancia_maxima) * ancho_util

    def convertir_y(self, altitud, altitud_minima, altitud_maxima):
        alto_util = self.alto - self.margen_superior - self.margen_inferior
        if altitud_maxima == altitud_minima:
            return self.margen_superior + alto_util / 2
        return self.margen_superior + (
            (altitud_maxima - altitud) / (altitud_maxima - altitud_minima)
        ) * alto_util

    def generar_svg(self, datos):
        distancia_maxima = max(dato[0] for dato in datos)
        altitud_minima = min(dato[1] for dato in datos)
        altitud_maxima = max(dato[1] for dato in datos)

        # Redondear la escala vertical a centenas para que sea legible.
        altitud_minima_escala = max(0, int(math.floor(altitud_minima / 100) * 100))
        altitud_maxima_escala = int(math.ceil(altitud_maxima / 100) * 100)
        if altitud_maxima_escala == altitud_minima_escala:
            altitud_maxima_escala += 100

        puntos = []
        for distancia, altitud, _ in datos:
            x = self.convertir_x(distancia, distancia_maxima)
            y = self.convertir_y(altitud, altitud_minima_escala, altitud_maxima_escala)
            puntos.append(f"{x:.2f},{y:.2f}")

        x0 = self.margen_izquierdo
        x1 = self.ancho - self.margen_derecho
        y0 = self.margen_superior
        y1 = self.alto - self.margen_inferior
        polilinea = " ".join(puntos)
        poligono_suelo = f"{x0},{y1} {polilinea} {x1},{y1}"

        lineas = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.ancho}" height="{self.alto}" viewBox="0 0 {self.ancho} {self.alto}">',
            '<rect width="100%" height="100%" fill="white"/>',
            '<text x="600" y="28" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold">Perfil altimétrico de la etapa</text>',
        ]

        # Cuadrícula y etiquetas verticales de altitud.
        paso_altitud = 200
        for altitud in range(altitud_minima_escala, altitud_maxima_escala + 1, paso_altitud):
            y = self.convertir_y(altitud, altitud_minima_escala, altitud_maxima_escala)
            lineas.append(f'<line x1="{x0}" y1="{y:.2f}" x2="{x1}" y2="{y:.2f}" stroke="#d7d7d7" stroke-width="1"/>')
            lineas.append(f'<text x="{x0 - 12}" y="{y + 5:.2f}" text-anchor="end" font-family="Arial" font-size="13">{altitud} m</text>')

        # Marcas horizontales cada 10 km.
        for distancia in range(0, int(distancia_maxima) + 1, 10):
            x = self.convertir_x(distancia, distancia_maxima)
            lineas.append(f'<line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y1}" stroke="#eeeeee" stroke-width="1"/>')
            lineas.append(f'<text x="{x:.2f}" y="{y1 + 22}" text-anchor="middle" font-family="Arial" font-size="12">{distancia}</text>')

        lineas.extend([
            f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="black" stroke-width="2"/>',
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="black" stroke-width="2"/>',
            f'<polygon points="{poligono_suelo}" fill="#dce8d1" stroke="none"/>',
            f'<polyline points="{polilinea}" fill="none" stroke="#426b37" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>',
            f'<text x="{(x0 + x1) / 2}" y="{self.alto - 24}" text-anchor="middle" font-family="Arial" font-size="16">Distancia desde la salida (km)</text>',
            f'<text x="22" y="{(y0 + y1) / 2}" transform="rotate(-90 22 {(y0 + y1) / 2})" text-anchor="middle" font-family="Arial" font-size="16">Altitud (m)</text>',
        ])

        # Etiquetar salida, llegada y puertos destacados.
        nombres_destacados = []
        for distancia, altitud, nombre in datos:
            if distancia == 0 or abs(distancia - distancia_maxima) < 0.001 or "Puerto" in nombre or "Pandera" in nombre:
                nombres_destacados.append((distancia, altitud, nombre))
        for distancia, altitud, nombre in nombres_destacados:
            x = self.convertir_x(distancia, distancia_maxima)
            y = self.convertir_y(altitud, altitud_minima_escala, altitud_maxima_escala)
            etiqueta = escape(nombre)
            lineas.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#b22222"/>')
            lineas.append(f'<text x="{x:.2f}" y="{y - 10:.2f}" text-anchor="middle" font-family="Arial" font-size="11" fill="#222">{etiqueta}</text>')

        lineas.append("</svg>")
        return "\n".join(lineas)

    def guardar_svg(self, archivo_svg):
        datos = self.obtener_datos()
        contenido = self.generar_svg(datos)
        with open(archivo_svg, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    def ejecutar(self, archivo_svg):
        self.guardar_svg(archivo_svg)


if __name__ == "__main__":
    programa = Xml2Altimetria("etapaEsquema.xml")
    programa.ejecutar("altimetria.svg")
    print("Archivo altimetria.svg generado correctamente.")

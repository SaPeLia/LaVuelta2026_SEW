
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


class Xml2Kml:

    def __init__(self, archivoXML):
        self.arbol = ET.parse(archivoXML)
        self.raiz = self.arbol.getroot()

        self.ns = {
            "u": "http://www.uniovi.es"
        }

    def obtenerCoordenadas(self, punto):
        longitud = punto.find("u:longitud", self.ns).text.strip()
        latitud = punto.find("u:latitud", self.ns).text.strip()
        altitud = punto.find("u:altitud", self.ns).text.strip()

        return f"{longitud},{latitud},{altitud}"

    def obtenerTexto(self, elemento, atributo, defecto):
        """Obtiene un atributo o devuelve un texto por defecto."""
        return elemento.get(atributo, defecto)

    def generarKml(self):

        kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Etapa de ciclismo</name>

    <Style id="rojo">
        <IconStyle>
            <color>ff0000ff</color>
        </IconStyle>
    </Style>

    <Style id="verde">
        <IconStyle>
            <color>ff00ff00</color>
        </IconStyle>
    </Style>

    <Style id="azul">
        <IconStyle>
            <color>ffff0000</color>
        </IconStyle>
    </Style>

    <Style id="amarillo">
        <IconStyle>
            <color>ff00ffff</color>
        </IconStyle>
    </Style>
"""

        # Salida
        salida = self.raiz.find(
            "./u:ciudadSalida",
            self.ns
        )
        puntoSalida = salida.find("u:puntoGeografico", self.ns)

        kml += f"""
    <Placemark>
        <name>{escape(salida.get("nombre", "Salida"))}</name>
        <styleUrl>#rojo</styleUrl>
        <Point>
            <coordinates>{self.obtenerCoordenadas(puntoSalida)}</coordinates>
        </Point>
    </Placemark>
"""

        # Llegada
        llegada = self.raiz.find(
            "./u:ciudadLlegada",
            self.ns
        )
        puntoLlegada = llegada.find("u:puntoGeografico", self.ns)

        kml += f"""
    <Placemark>
        <name>{escape(llegada.get("nombre", "Llegada"))}</name>
        <styleUrl>#rojo</styleUrl>
        <Point>
            <coordinates>{self.obtenerCoordenadas(puntoLlegada)}</coordinates>
        </Point>
    </Placemark>
"""

        # Recopilar los puntos con su distancia acumulada.
        # Cada elemento de la lista es: (distancia, nombre, puntoGeografico).
        puntosRecorrido = [
            (
                0.0,
                salida.get("nombre", "Salida"),
                puntoSalida
            )
        ]

        # Hitos: puertos y sprints
        hitos = self.raiz.findall(
            "./u:hitos/u:hito",
            self.ns
        )

        for hito in hitos:
            distanciaElemento = hito.find(
                "u:distanciaDesdeSalida",
                self.ns
            )
            punto = hito.find("u:puntoGeografico", self.ns)

            distancia = float(distanciaElemento.text.strip())

            puerto = hito.find("u:puerto", self.ns)
            sprint = hito.find("u:sprint", self.ns)

            if puerto is not None:
                nombre = self.obtenerTexto(
                    puerto, "nombre", "Puerto"
                )
                estilo = "verde"
            else:
                nombre = "Sprint intermedio"
                estilo = "azul"

            kml += f"""
    <Placemark>
        <name>{escape(nombre)}</name>
        <styleUrl>#{estilo}</styleUrl>
        <Point>
            <coordinates>{self.obtenerCoordenadas(punto)}</coordinates>
        </Point>
    </Placemark>
"""

            puntosRecorrido.append((distancia, nombre, punto))

        # Puntos anónimos: máximo 30
        anonimos = self.raiz.findall(
            "./u:puntosAnónimos/u:puntoAnónimo",
            self.ns
        )

        for anonimo in anonimos[:30]:
            distanciaElemento = anonimo.find(
                "u:distanciaDesdeSalida",
                self.ns
            )
            punto = anonimo.find("u:puntoGeografico", self.ns)

            distancia = float(distanciaElemento.text.strip())
            nombre = anonimo.get("nombre", "Punto anónimo")

            kml += f"""
    <Placemark>
        <name>{escape(nombre)}</name>
        <styleUrl>#amarillo</styleUrl>
        <Point>
            <coordinates>{self.obtenerCoordenadas(punto)}</coordinates>
        </Point>
    </Placemark>
"""

            puntosRecorrido.append((distancia, nombre, punto))

        # Añadir la meta al recorrido
        longitud = self.raiz.find(
            "./u:longitud",
            self.ns
        )
        distanciaFinal = float(longitud.text.strip())

        puntosRecorrido.append((
            distanciaFinal,
            llegada.get("nombre", "Llegada"),
            puntoLlegada
        ))

        # Ordenar por distancia desde la salida
        puntosRecorrido.sort(key=lambda elemento: elemento[0])

        # Línea del recorrido
        kml += """
    <Placemark>
        <name>Recorrido de la etapa</name>
        <Style>
            <LineStyle>
                <color>ff0000ff</color>
                <width>4</width>
            </LineStyle>
        </Style>
        <LineString>
            <tessellate>1</tessellate>
            <coordinates>
"""

        for distancia, nombre, punto in puntosRecorrido:
            kml += "                "
            kml += self.obtenerCoordenadas(punto) + "\n"

        kml += """            </coordinates>
        </LineString>
    </Placemark>
</Document>
</kml>
"""

        return kml

    def guardarKml(self, archivoKml):
        kml = self.generarKml()

        with open(archivoKml, "w", encoding="UTF-8") as archivo:
            archivo.write(kml)


# Programa principal
if __name__ == "__main__":
    programa = Xml2Kml("etapaEsquema.xml")
    programa.guardarKml("etapa.kml")

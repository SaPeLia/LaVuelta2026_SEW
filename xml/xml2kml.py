import xml.etree.ElementTree as ET


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

        return longitud + "," + latitud + ",0"

    def generarKml(self):

        kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>

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

        # --------------------------------------------------
        # SALIDA
        # --------------------------------------------------

        salida = self.raiz.find(
            ".//u:ciudadSalida/u:puntoGeografico",
            self.ns
        )

        coordenadas = self.obtenerCoordenadas(salida)

        kml += f"""
<Placemark>
    <name>Salida</name>
    <styleUrl>#rojo</styleUrl>
    <Point>
        <coordinates>{coordenadas}</coordinates>
    </Point>
</Placemark>
"""

        # --------------------------------------------------
        # LLEGADA
        # --------------------------------------------------

        llegada = self.raiz.find(
            ".//u:ciudadLlegada/u:puntoGeografico",
            self.ns
        )

        coordenadas = self.obtenerCoordenadas(llegada)

        kml += f"""
<Placemark>
    <name>Llegada</name>
    <styleUrl>#rojo</styleUrl>
    <Point>
        <coordinates>{coordenadas}</coordinates>
    </Point>
</Placemark>
"""

        # --------------------------------------------------
        # PUERTOS
        # --------------------------------------------------

        puertos = self.raiz.findall(
            ".//u:hitos/u:hito[u:puerto]/u:puntoGeografico",
            self.ns
        )

        for punto in puertos:

            coordenadas = self.obtenerCoordenadas(punto)

            kml += f"""
<Placemark>
    <name>Puerto</name>
    <styleUrl>#verde</styleUrl>
    <Point>
        <coordinates>{coordenadas}</coordinates>
    </Point>
</Placemark>
"""

        # --------------------------------------------------
        # SPRINTS
        # --------------------------------------------------

        sprints = self.raiz.findall(
            ".//u:hitos/u:hito[u:sprint]/u:puntoGeografico",
            self.ns
        )

        for punto in sprints:

            coordenadas = self.obtenerCoordenadas(punto)

            kml += f"""
<Placemark>
    <name>Sprint</name>
    <styleUrl>#azul</styleUrl>
    <Point>
        <coordinates>{coordenadas}</coordinates>
    </Point>
</Placemark>
"""

        # --------------------------------------------------
        # PUNTOS ANÓNIMOS
        # --------------------------------------------------

        anonimos = self.raiz.findall(
            ".//u:puntosAnónimos/u:puntoAnónimo/u:puntoGeografico",
            self.ns
        )

        # Máximo 30 puntos
        anonimos = anonimos[:30]

        for punto in anonimos:

            coordenadas = self.obtenerCoordenadas(punto)

            kml += f"""
<Placemark>
    <name>Punto anónimo</name>
    <styleUrl>#amarillo</styleUrl>
    <Point>
        <coordinates>{coordenadas}</coordinates>
    </Point>
</Placemark>
"""

        # --------------------------------------------------
        # LÍNEA DEL RECORRIDO
        # --------------------------------------------------

        puntos = self.raiz.findall(
            ".//u:puntoGeografico",
            self.ns
        )

        kml += """
<Placemark>
    <name>Recorrido</name>
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

        for punto in puntos:

            coordenadas = self.obtenerCoordenadas(punto)

            kml += coordenadas + "\n"

        kml += """
        </coordinates>
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


# ------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------

programa = Xml2Kml("etapaEsquema.xml")
programa.guardarKml("etapa.kml")

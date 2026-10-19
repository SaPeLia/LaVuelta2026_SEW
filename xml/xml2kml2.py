import xml.etree.ElementTree as ET

def xml2kml(archivoXML):
    try:
        
        arbol = ET.parse(archivoXML)
        
    except IOError:
        print ('No se encuentra el archivo ', archivoXML)
        exit()
        
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", archivoXML)
        exit()
       
    raiz = arbol.getroot()
    
    print("\nElemento raiz = ", raiz.tag)

    if raiz.text != None:
        print("Contenido = "    , raiz.text.strip('\n')) #strip() elimina los '\n' del string
    else:
        print("Contenido = "    , raiz.text)
        
    print("Atributos = "    , raiz.attrib)

    # Recorrido de los elementos del árbol
    puntos = raiz.findall(
                ".//u:puntoGeografico",
                "http://www.uniovi.es"
            )
    for punto in puntos: # Expresión Path
        longitud = punto.find("u:longitud", self.ns).text.strip()
        latitud = punto.find("u:latitud", self.ns).text.strip()
        
        addPlacemark()    

def addPlacemark(self,nombre,descripcion,long,lat,alt, modoAltitud):
        """
        Añade un elemento <Placemark> con puntos <Point>
        """
        pm = ET.SubElement(self.doc,'Placemark')
        ET.SubElement(pm,'name').text = nombre
        ET.SubElement(pm,'description').text = descripcion
        punto = ET.SubElement(pm,'Point')
        ET.SubElement(punto,'coordinates').text = '{},{},{}'.format(long,lat,alt)
        ET.SubElement(punto,'altitudeMode').text = modoAltitud

def addLineString(self,nombre,extrude,tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento <Placemark> con líneas <LineString>
        """
        ET.SubElement(self.doc,'name').text = nombre
        pm = ET.SubElement(self.doc,'Placemark')
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls,'extrude').text = extrude
        ET.SubElement(ls,'tessellation').text = tesela
        ET.SubElement(ls,'coordinates').text = listaCoordenadas
        ET.SubElement(ls,'altitudeMode').text = modoAltitud 

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement (linea, 'color').text = color
        ET.SubElement (linea, 'width').text = ancho

def escribir(self,nombreArchivoKML):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)
    
def ver(self):
        """
    Muestra el archivo KML. Se utiliza para depurar
        """
        print("\nElemento raiz = ", self.raiz.tag)

        if self.raiz.text != None:
            print("Contenido = "    , self.raiz.text.strip('\n')) #strip() elimina los '\n' del string
        else:
            print("Contenido = "    , self.raiz.text)
        
        print("Atributos = "    , self.raiz.attrib)

        # Recorrido de los elementos del árbol
        for hijo in self.raiz.findall('.//'): # Expresión XPath
            print("\nElemento = " , hijo.tag)
            if hijo.text != None:
                print("Contenido = ", hijo.text.strip('\n')) #strip() elimina los '\n' del string
            else:
                print("Contenido = ", hijo.text)    
            print("Atributos = ", hijo.attrib)

def main():
    """Prueba de la función verXML()"""
        
    print(verXML.__doc__)
        
    miArchivoXML = "etapaEsquenma.xml"

    """Prueba unitaria de la clase Kml"""
    
    """ nombreKML = input('Introduzca el nombre del archivo KML = ') """

    nombreKML = "etapa.kml"

    nuevoKML = Kml()
      
    """Visualización del KML creado"""
    nuevoKML.ver()
    
    """Creación del archivo en formato KML"""
    nuevoKML.escribir(nombreKML)
    print("Creado el archivo: ", nombreKML)
    
if __name__ == "__main__":
    main()
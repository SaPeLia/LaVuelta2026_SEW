
class Ciudad {
    nombre = null;
    pais = null;
    gentilicio = null;
    poblacion = null;
    coordenadas = null;
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;
        this.poblacion = null;
        this.coordenadas = null;
    }

    rellenarAtributos() {
        this.poblacion = 111888;
        this.coordenadas = "37.7650, -3.7903";
    }

    getCiudad() {
        return this.nombre;
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        return `
            <ul>
                <li>Gentilicio: ${this.gentilicio}</li>
                <li>Población: ${this.poblacion} habitantes</li>
            </ul>
        `;
    }

    escribeCoordenadas() {
        let seccion = document.querySelector("main section");

        let parrafo = document.createElement("p");
        parrafo.textContent = "Coordenadas: " + this.coordenadas;
        seccion.appendChild(parrafo);
    }

}

let ciudad = new Ciudad("Jaén", "España", "jiennense");

ciudad.rellenarAtributos();

let seccion = document.createElement("section");

let encabezado = document.createElement("h3");
encabezado.textContent = ciudad.getCiudad() + ", " + ciudad.getPais();

seccion.appendChild(encabezado);

seccion.insertAdjacentHTML("beforeend", ciudad.getInformacionSecundaria());

let encabezadoMeteorologia = document.querySelector("main h2");

encabezadoMeteorologia.insertAdjacentElement("afterend", seccion);

ciudad.escribeCoordenadas();

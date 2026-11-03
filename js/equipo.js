
class Equipo {
    nombre = null;
    codigoUCI = null;
    pais = null;
    director = null;
    categoria = null;
    paginaWeb = null;
    constructor(nombre, codigoUCI, pais) {
        this.nombre = nombre;
        this.codigoUCI = codigoUCI;
        this.pais = pais;

    }
    rellenarAtributos() {
        this.director = "Thierry Bricaud / Vaugrenard Benoit";
        this.categoria = "UCI WorldTeam";
        this.paginaWeb = "https://www.lavuelta.es/es/equipo/GFC/groupama-fdj-united";
    }
    datosBasicos() {
        return this.nombre + " (" + this.codigoUCI + ")";
    }
    getPais() {
        return this.pais;
    }
    getInformacionSecundaria() {
        return `
        <ul>
            <li>Director: ${this.director}</li>
            <li>Categoría: ${this.categoria}</li>
        </ul>
    `;
    }
    getPaginaWeb() {
        let seccion = document.querySelector("main section");

        let enlace = document.createElement("a");
        enlace.href = this.paginaWeb;
        enlace.textContent = "Página web del equipo en La Vuelta";

        let parrafo = document.createElement("p");
        parrafo.appendChild(enlace);

        seccion.appendChild(parrafo);
    }

}
let equipo = new Equipo("Groupama-FDJ United", "GFC", "Francia");

equipo.rellenarAtributos();


let seccion = document.createElement("section");


let encabezado = document.createElement("h3");
encabezado.textContent = equipo.datosBasicos() + " - " + equipo.getPais();

seccion.appendChild(encabezado);

seccion.insertAdjacentHTML("beforeend", equipo.getInformacionSecundaria());

let encabezadoEquipo = document.querySelector("main h2");
encabezadoEquipo.insertAdjacentElement("afterend", seccion);


equipo.getPaginaWeb();

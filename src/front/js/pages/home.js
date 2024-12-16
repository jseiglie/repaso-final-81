import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { Formulario } from "../component/formulario.jsx";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
						<div className="container bg-danger">
				verificar si tienes usuarios, libros o libros, sino no podras hacer mucho. Crealos ya que las base de datos estan ancladas a los codespaces, los que creamos en clase, no estan aqui 
			</div>
		<h2>REGISTER</h2>
		<Formulario type={'register'}/>


		<h2>LOGIN</h2>
		<Formulario type={'login'}/>
	

		{store.books?.map(el=> <p key={el.id}>{el.title}</p>)}


		</div>
	);
};

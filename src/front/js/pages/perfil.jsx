import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";


export const Perfil = () => {

    const navigate = useNavigate()

    const {store, actions} = useContext(Context);

    useEffect(()=>{
        if (!localStorage.getItem('token')) navigate('/')
        if (!store.user) actions.getUserInfo()
    },[store.user])



    return (
        <section>
            <h2>Perfil</h2>
            <p>correo: {store.user?.email}</p>
            <button onClick={actions.logout}>logout</button>
        </section>
    )
}
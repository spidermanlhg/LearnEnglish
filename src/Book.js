import React from 'react'
import { Routes, Route } from 'react-router-dom'
import axios from 'axios'

function Book(){

    const clickHandler=()=>{

        axios.get( 'http://127.0.0.1:8000/hello/lhg/90' )

    }


    return  (
        <div>
            <button onClick={ clickHandler } >Click</button>
        </div>
    )


}


export default Book
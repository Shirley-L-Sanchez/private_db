import React from 'react';
import {useLocation} from 'react-router-dom';
import {useState, useEffect} from 'react'

function QueryResult() {
    const query = useLocation().state.result;
    let [queryResult, setQueryResult] = useState("")

    let getQueryResult = async () => {
        let response = await fetch(
            "http://localhost:3000/who_request", 
            {method: "POST",
            mode:"cors",
            headers: {"Content-type":"application/json;charset=utf-8"},
            body: JSON.stringify({"query": query})}
            )
        response = await response.json()
        if (response.who === "None"){
            //CASE 1: INVALID QUERY
            console.log("CASE 1")
            setQueryResult("Invalid query :(")
        }
        else if (response.who === "gdb"){
            //CASE 2: QUERY ON PUBLIC DATA
            console.log("CASE 2")
            setQueryResult(response.queryResult)
        } else if (response.who == "system"){
            //CASE 3: AGGREGATE QUERY ON PRIVATE DATA
            console.log("CASE 3")
            setQueryResult(response.queryResult)
        }
        else {
            //get user -- just for testing purposes, we will default to user 1
            //CASE 4: GET PRIVATE DATA
            console.log("CASE 4")
            let response = await fetch(
                "http://localhost:5000/private_request", 
                {method: "POST",
                mode:"cors",
                headers: {"Content-type":"application/json;charset=utf-8"},
                body: JSON.stringify({"query": query})}
                )
            response = await response.json()
            console.log(response.who)
            if (response.who == "None"){
                console.log("CASE 4.1")
                setQueryResult("Invalid Query :( - this should not happen")
            } 
            else if (response.who == "mdb"){
                setQueryResult(response.queryResult)
            } else {
                console.log("HERE!")
            }
        }
    }
    

    console.log("Extracted query state from previous link:", query)
    getQueryResult()
    console.log("Reached this point")
    console.log("This is the query result: ", queryResult)

    return (
    <div><p>{queryResult}</p></div>
    )
}

export default QueryResult
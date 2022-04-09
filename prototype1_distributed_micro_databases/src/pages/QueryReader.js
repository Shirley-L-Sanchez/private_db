import React, {useState, useEffect} from 'react'
import {Link} from 'react-router-dom'
import '../tailwind.css';


export const QueryReader = () => {

    let [query, setQuery] = useState("")


    return (
        <div class="my-14 mx-14 overflow-auto">
            <h4 class="
                font-medium leading-tight text-3xl
                px-1.5 mt-0 mb-2 text-blue-500">
            SQL Query Reader
            </h4>
            <div class="container " width="1000">
                <textarea
                    class="
                    my-3 w-full h-80 px-3
                    py-2 text-lg font-normal text-gray-700 
                    bg-white bg-clip-padding border
                    border-solid border-gray-300
                    rounded transition ease-in-out
                    m-0 focus:text-gray-700 focus:bg-white
                    focus:border-blue-500 focus:outline-none"
                    id="text-area"
                    rows="3"
                    onChange= 
                    {(e) => 
                        { 
                        setQuery(e.target.value)
                        }
                    }
                    value={query} 
                    placeholder="Write your query here">
                </textarea>
                <Link 
                to={{pathname: '/queryResult', state: {result: query}}}
                replace={false}>
                    <button
                        type="button"
                        data-mdb-ripple="true"
                        data-mdb-ripple-color="light"
                        class="
                        px-6 py-2.5 bg-blue-500 text-white
                        font-medium text-base leading-tight
                        uppercase rounded shadow-md hover:bg-blue-700
                        hover:shadow-lg focus:bg-blue-700 focus:shadow-lg
                        focus:outline-none focus:ring-0 active:bg-blue-800
                        active:shadow-lg transition duration-150 ease-in-out"
                        >
                        Execute query
                    </button>
                </Link>
            </div>
        </div>
    )
}

export default QueryReader;
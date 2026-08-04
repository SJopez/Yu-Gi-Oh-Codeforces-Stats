import Card from './card'
import './menu.css'
import { useEffect, useRef, useState } from 'react'
import DuelDisk from './disk';

export interface CodeforcesUser {
    handle: string;
    max_rank: string;
    rank: string;
    max_rating: number;
    rating: number;
    avatar: string;
    type: string;
    most_used_lang: string;
    badges: Array<string>;
}
interface Input {
    onchange: (user: string) => void;
}
interface MenuOptions {
    width: number;
}

export async function handleSubmit(user: string, change: Function) {
    const response = await fetch("https://yu-gi-oh-codeforces-stats.onrender.com/user.info?handle="+user)
    if(!response.ok) throw new Error("Something went wrong!")
    const data = await response.json()
    const result = data as CodeforcesUser
    change(result)
}

function InputField(props: Input) {
    let currInput = useRef<HTMLInputElement>(null);

    return (
        <div id='inputContainer'>
            <input ref={currInput} id='inputField' type="text" placeholder='Enter your username...' defaultValue={"Tourist"}></input>
            <button id='inputButton' onClick={() => props.onchange(currInput.current?.value!)}>Submit</button>
        </div>
    )
}

export default function Menu(props: MenuOptions) {
    let [username, setUsername] = useState("tourist")
    let menu = useRef<HTMLDivElement>(null)
    let [width, setWidth] = useState(0)

    useEffect(() => {
        if (menu.current) setWidth(menu.current.offsetWidth)
    }, [])

    return (
        <div id='menu' ref={menu}>
            <InputField onchange={setUsername}></InputField>
            <Card 
                username={username}
                width={props.width}
                preffix=''
                scale={false}
                info={true}>     
            </Card>
            <DuelDisk width={width}></DuelDisk>
        </div>
    )
}

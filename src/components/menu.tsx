import Card from './card'
import './menu.css'
import { useRef, useState } from 'react'
import DuelDisk from './disk';

export interface CodeforcesUser {
    handle: string;
    rank: string;
    rating: number;
    titlePhoto: string;
    type: string;
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
    const result = data.result[0] as CodeforcesUser
    
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

    return (
        <div id='menu'>
            <InputField onchange={setUsername}></InputField>
            <Card 
                username={username}
                stars={8}
                width={props.width}
                preffix=''
                scale={false}
                info={true}>     
            </Card>
            <DuelDisk width={props.width}></DuelDisk>
        </div>
    )
}

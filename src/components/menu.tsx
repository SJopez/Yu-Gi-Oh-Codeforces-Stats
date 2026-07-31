import Card from './card'
import './menu.css'
import { useRef, useState } from 'react'
import Metrics from '../metrics.json'

interface CodeforcesUser {
    handle: string;
    rank: string;
    rating: number;
    titlePhoto: string;
    type: string;
}
interface Input {
    onchange: (user: CodeforcesUser) => void;
}

function InputField(props: Input) {
    var currInput = useRef<HTMLInputElement>(null);

    async function handleSubmit() {
        
        const user = currInput.current?.value
        const response = await fetch("https://codeforces.com/api/user.info?handles="+user)
        if(!response.ok) throw new Error("Something went wrong!")
        const data = await response.json()
        const result = data.result[0] as CodeforcesUser
        
        props.onchange(result)
    }
    return (
        <div id='inputContainer'>
            <input ref={currInput} id='inputField' type="text" placeholder='Enter your username...'></input>
            <button id='inputButton' onClick={handleSubmit}>Submit</button>
        </div>
    )

}

export default function Menu() {
    var [username, setUsername] = useState("Tourist")
    var [type, setType] = useState("Legendary Grandmaster")
    var [rank, setRank] = useState("legendary_grandmaster")
    var [photo, setPhoto] = useState("/src/assets/cards/tourist.jpg")
    var [glow, setGlow] = useState(true)
    var [sparkle, setSparkle] = useState(true)
    var [effectOpacity, setEffectOpacity] = useState(0.6)
    var [nameEffect, setNameEffect] = useState(true)
    
    function change(user: CodeforcesUser) {
        type Rank = keyof typeof Metrics
        const rankIndex = user.rank as Rank
        const config = Metrics[rankIndex]

        setUsername(user.handle)
        setRank(config.rankName)
        setPhoto(user.titlePhoto)
        setType(user.type)
        setGlow(config.glow)
        setSparkle(config.sparkle)
        setEffectOpacity(config.effectOpacity)
        setNameEffect(config.nameEffect)
    }

    return (
        <div id='menu'>
            <InputField onchange={change}></InputField>
            <Card 
                username={username} 
                starts={8} 
                type={type} 
                attack={4000} 
                defense={1200} 
                rank={rank} 
                photo={photo} 
                glow={glow} 
                sparkle={sparkle} 
                effectOpacity={effectOpacity}
                nameEffect={nameEffect}         
                >     
            </Card>
        </div>
    )

}
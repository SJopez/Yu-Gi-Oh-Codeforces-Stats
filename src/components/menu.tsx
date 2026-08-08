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
    solved_problemes: number;
    tags: Array<Array<number | string>>;
    rank_pos: number;
    contr_pos: number;
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
        <div id='inputWrapper'>
            <div id='inputContainer'>
                <input
                    ref={currInput}
                    id='inputField'
                    type="text"
                    placeholder='Enter your username...'
                    defaultValue={"Tourist"}
                />
                <button id='inputButton' onClick={() => props.onchange(currInput.current?.value!)}>
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
                        <line x1="16.5" y1="16.5" x2="21" y2="21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                </button>
            </div>
        </div>
    )
}

async function fetchTops(rankSetter: (list: Array<CodeforcesUser>) => void, 
                         contriSetter: (list: Array<CodeforcesUser>) => void){
    const response = await fetch("https://yu-gi-oh-codeforces-stats.onrender.com/tops")
    if(!response.ok) throw new Error("Something went wrong!")
    const data = await response.json()
    const rank = data.top_rated as Array<CodeforcesUser>
    const contri = data.top_contributors as Array<CodeforcesUser>
    rankSetter(rank)
    contriSetter(contri)
}

export default function Menu(props: MenuOptions) {
    let [username, setUsername] = useState("tourist")
    let menu = useRef<HTMLDivElement>(null)
    let [rankUsernameList, setRankUsernameList] = useState<Array<CodeforcesUser>>([]) 
    let [contriUsernameList, setContriUsernameList] = useState<Array<CodeforcesUser>>([])
    let [width, setWidth] = useState(0)

    useEffect(() => {
        if (menu.current) setWidth(menu.current.offsetWidth)
            
        if (rankUsernameList.length == 0 && contriUsernameList.length == 0){
            fetchTops(setRankUsernameList, setContriUsernameList)
        }
    }, [props.width])

    return (
        <div id='menu' ref={menu}>
            <h1 id='menuTitle'>
                Yu-Gi-Oh! <span>Codeforces Stats</span>
            </h1>
            <InputField onchange={setUsername}></InputField>
            <Card 
                username={username}
                width={props.width}
                preffix=''
                scale={false}
                info={true}
                rankRating={rankUsernameList}
                contributionRank={contriUsernameList}>     
            </Card>
            <DuelDisk width={width} ratingRank={rankUsernameList!} contributionRank={contriUsernameList!}></DuelDisk>
        </div>
    )
}

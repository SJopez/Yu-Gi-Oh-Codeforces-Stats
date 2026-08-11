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
    solved_problems: number;
    tags: Array<Array<number | string>>;
    rated_pos: number;
    contr_pos: number;
}

interface Input {
    onchange: (user: string) => void;
}
interface MenuOptions {
    width: number;
}

export async function handleSubmit(user: string, change: Function, setter: (value: boolean) => void) {
    try {
        setter(true)
        const response = await fetch("https://yu-gi-oh-codeforces-stats.onrender.com/user.info?handle="+user)
        if(!response.ok) throw new Error("Something went wrong!")
        const data = await response.json()
        const result = data as CodeforcesUser
        change(result)
    } catch (error) {
        setter(false)
    }
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

function GithubLink() {
    return (
        <a       
            id='githubLink'
            href='https://github.com/SJopez/Yu-Gi-Oh-Codeforces-Stats'
            target='_blank'
            rel='noopener noreferrer'
            aria-label='Ver repositorio en GitHub'
        >
            <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 0C5.37 0 0 5.5 0 12.3c0 5.44 3.44 10.05 8.21 11.68.6.11.82-.27.82-.6 0-.29-.01-1.06-.02-2.08-3.34.75-4.04-1.66-4.04-1.66-.55-1.42-1.34-1.8-1.34-1.8-1.09-.77.08-.75.08-.75 1.21.09 1.84 1.27 1.84 1.27 1.07 1.87 2.81 1.33 3.5 1.02.11-.79.42-1.33.76-1.64-2.66-.31-5.47-1.36-5.47-6.05 0-1.34.46-2.43 1.22-3.29-.12-.31-.53-1.56.12-3.25 0 0 1-.33 3.3 1.26a11.2 11.2 0 0 1 3-.41c1.02 0 2.04.14 3 .41 2.28-1.59 3.29-1.26 3.29-1.26.65 1.69.24 2.94.12 3.25.76.86 1.22 1.95 1.22 3.29 0 4.7-2.81 5.74-5.49 6.04.43.38.81 1.13.81 2.29 0 1.65-.02 2.98-.02 3.39 0 .33.22.72.83.6C20.57 22.34 24 17.74 24 12.3 24 5.5 18.63 0 12 0z"/>
            </svg>
        </a>
    )
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
            <GithubLink></GithubLink>
            <Card 
                username={username}
                width={props.width}
                preffix=''
                scale={false}
                info={true}
                rankRating={rankUsernameList}
                contributionRank={contriUsernameList}>     
            </Card>
            <DuelDisk width={width} ratingRank={rankUsernameList!} contributionRank={contriUsernameList!} nameSetter={setUsername}></DuelDisk>
        </div>
    )
}

const images = import.meta.glob('/src/assets/*.{png,jpg}', { eager: true, import: 'default' });
import { useEffect, useRef, useState } from 'react';
import Card from './card';
import './disk.css'

interface DiskOptions {
    width: number
}

export default function DuelDisk(props: DiskOptions){
    let usernameList = ["sergio22", "sn0wm4n", "itadrias", "EduardoBrito", "jiangly"]
    let cardList = []
    let container = useRef<HTMLDivElement>(null)
    let [width, setWidth] = useState(0)

    useEffect(() => {
        if (container.current) {
            var perc = window.innerWidth * 0.3
            container.current.style.width = Math.max(400, perc) + "px"
            setWidth(container.current.offsetWidth)

        }
         
    }, [])

    for (let i = 0; i < 5; i++){
        let user = usernameList[i]
        
        cardList.push(
            <Card 
                username={user}
                stars={1}
                preffix={`mini${i + 1}`}
                width={width}
                scale={true}>     
            </Card>
        )
    }

    return (
        <div id="diskContainer" ref={container}>
            <img id='diskImage' src={`${images["/src/assets/character.png"]}`}></img>
            {cardList}                     
        </div>
    )
}
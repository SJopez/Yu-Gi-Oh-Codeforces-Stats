import { useEffect, useRef, useState } from 'react';
import './card.css'
import { handleSubmit, type CodeforcesUser } from './menu';
const images = import.meta.glob('/src/assets/cards/*.{png,jpg}', { eager: true, import: 'default' });
const effects = import.meta.glob('/src/assets/cards/effects/*.png', { eager: true, import: 'default' });
import Metrics from '../metrics.json'

interface FetchProps {
    username: string;
    stars: number;
    width: number;
    preffix: string;
    scale?: Boolean;
} 

function Attribute(){
    return (
        <div id='langContainer'>
            <img id="attribute" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-plain.svg" />
        </div>
    )
}

export function Sparkle() {
  return (
    <div className="sparkle">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
  );
}

export function CardGlow() {
  return (
    <svg className="card-glow" viewBox="0 0 408 612">
      <rect
        className="card-glow-path"
        x="23"
        y="42"
        width="360"
        height="520"
        rx="13"
      />
    </svg>
  );
}

export default function Card(props: FetchProps) {
    var starArray = []
    var name = useRef<HTMLHeadingElement>(null)
    var cardContainer = useRef<HTMLDivElement>(null)
    var [type, setType] = useState("Legendary Grandmaster")
    var [rank, setRank] = useState("legendary_grandmaster")
    var [photo, setPhoto] = useState("https://userpic.codeforces.org/422/title/50a270ed4a722867.jpg")
    var [glow, setGlow] = useState(true)
    var [sparkle, setSparkle] = useState(true)
    var [effectOpacity, setEffectOpacity] = useState(0.6)
    var [nameEffect, setNameEffect] = useState(true)

    useEffect(() => {
        handleSubmit(props.username, change)       
    }, [])
    
    function change(user: CodeforcesUser) {
        type Rank = keyof typeof Metrics
        const rankIndex = user.rank as Rank
        const config = Metrics[rankIndex]

        setRank(config.rankName)
        setPhoto(user.titlePhoto)
        setType(config.type)
        setGlow(config.glow)
        setSparkle(config.sparkle)
        setEffectOpacity(config.effectOpacity)
        setNameEffect(config.nameEffect)
    }

    useEffect(() => {
        if(name.current){
            if (nameEffect){
                name.current.classList.add('golden')
            }
            else {
                name.current.classList.remove('golden')
            }
        }
        if (cardContainer.current){
            if (props.scale){
                var scale = 0.24 * props.width / 800
                cardContainer.current.style.setProperty("--card-scale", scale.toString());
            }
            else if (props.width >= 408){
                cardContainer.current.style.setProperty("--card-scale", "1");
            }
            else {
                cardContainer.current.style.setProperty("--card-scale", (props.width / 408).toString());
            }
        }

    })
    
    for (var i = 0; i < Math.min(props.stars, 12); i++) {
        starArray.push(<img id={`start${i}`} className='star' src={images['/src/assets/cards/star.png'] as string}></img>)
    }

    return (
        <div className={props.preffix + 'cardContainer'} ref={cardContainer}>
            {glow && <CardGlow></CardGlow>}
            {sparkle && <Sparkle></Sparkle>}
            <img style={{opacity: effectOpacity}} id='effect' src={effects[`/src/assets/cards/effects/${rank}.png`] as string}></img>
            <img id='cardTemplate' src={images[`/src/assets/cards/${rank}.png`] as string}></img>
            <div id='nameContainer'>
                <h1 id='cardName' ref={name}>{props.username}</h1>
                <Attribute></Attribute>
            </div>
            <div id='starsContainer'>
                {starArray}
            </div>
            <div id='imageContainer' style = {{ backgroundImage: `url(${photo})` }}></div>
            <div id='textContainer'>
                <label id='cardType'> [{type}] </label>
                <div id='descriptionContainer' className='scrollable'>
                    <p id='description'>
                        Requires 3 Tributes to Normal Summon (cannot be Normal Set). This card's Normal Summon cannot be negated.  
                    </p>
                </div>
                <hr id='separator'></hr>
                <div id='statsContainer'>
                    <label id='atk'>ATK/{"4000"}</label>
                    <label id='def'>DEF/{"1200"}</label>
                </div>
            </div>
        </div>
    )
}
import { useEffect, useRef, useState } from 'react';
import './card.css'
import { handleSubmit, type CodeforcesUser } from './menu';
const images = import.meta.glob('/src/assets/cards/*.{png,jpg}', { eager: true, import: 'default' });
const effects = import.meta.glob('/src/assets/cards/effects/*.png', { eager: true, import: 'default' });
import Metrics from '../metrics.json'

interface FetchProps {
    username: string;
    width: number;
    preffix: string;
    scale?: Boolean;
    info?: Boolean;    
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
    let starArray = []
    let badgeArray = []
    let name = useRef<HTMLHeadingElement>(null)
    let cardContainer = useRef<HTMLDivElement>(null)
    let [handle, setHandle] = useState("")
    let [type, setType] = useState("Legendary Grandmaster")
    let [rank, setRank] = useState("legendary_grandmaster")
    let [photo, setPhoto] = useState("https://userpic.codeforces.org/422/title/50a270ed4a722867.jpg")
    let [glow, setGlow] = useState(true)
    let [sparkle, setSparkle] = useState(true)
    let [effectOpacity, setEffectOpacity] = useState(0.6)
    let [nameEffect, setNameEffect] = useState(true)
    let [className, setClassName] = useState("cardContainer")
    let [maxRank, setMaxRank] = useState("")
    let [rating, setRating] = useState(0)
    let [maxRating, setMaxRating] = useState(0)
    let [lang, setLang] = useState("")
    let [badgeList, setBadgeList] = useState(Array<string>())
    let [stars, setStars] = useState(0)
 
    useEffect(() => {
        if (props.scale) setClassName("miniCardContainer")
        handleSubmit(props.username, change)       
    })
    
    function change(user: CodeforcesUser) {
        type Rank = keyof typeof Metrics
        const maxRankIndex = user.max_rank as Rank
        const rankIndex = user.rank as Rank
        const config = Metrics[rankIndex]
        const maxRankConfig = Metrics[maxRankIndex]

        setHandle(user.handle)
        setRank(config.rankName)
        setMaxRank(user.max_rank)
        setRating(user.rating)
        setMaxRating(user.max_rating)
        setPhoto(user.avatar)
        setLang(user.most_used_lang)
        setType(config.type)
        setGlow(config.glow)
        setSparkle(config.sparkle)
        setEffectOpacity(config.effectOpacity)
        setNameEffect(config.nameEffect)
        setBadgeList(user.badges)
        

        if (maxRankConfig == undefined) setStars(12)
        else setStars(maxRankConfig.stars)
        
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
                let scale = 0.24 * props.width / 1000
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
    
    for (let i = 0; i < stars; i++) {
        starArray.push(<img id={`start${i}`} className='star' src={images['/src/assets/cards/star.png'] as string}></img>)
    }
    for (let i = 0; i < badgeList.length; i++){
        badgeArray.push(<img className='badge' src={badgeList[i]}></img>)
    }

    function CardInformation() {
        return (
            <div className="cardInfo">
                <div className="hudCorner hudCornerTopLeft" />
                <div className="hudCorner hudCornerTopRight" />
                <div className="hudCorner hudCornerBottomLeft" />
                <div className="hudCorner hudCornerBottomRight" />
                <div className="username">{handle}</div>
                <div className="statsList">
                    <div className="statLine">Rank: <span className="statValue">{type}r</span></div>
                    <div className="statLine">Max rank: <span className="statValue">{maxRank}</span></div>
                    <div className="statLine">Rating: <span className="statValue">{rating}</span></div>
                    <div className="statLine">Max rating: <span className="statValue">{maxRating}</span></div>
                    <div className="statLine">Problems solved: <span className="statValue">4127</span></div>
                    <div className="statLine">Most used lang: <span className="statValue">{lang}</span></div>
                </div>
            </div>
        );
    }

    return (
        <div className={props.preffix + 'totalContainer'}>
            <div id={props.preffix} className={className} ref={cardContainer}>
                {glow && <CardGlow></CardGlow>}
                {sparkle && <Sparkle></Sparkle>}
                <img style={{opacity: effectOpacity}} id='effect' src={effects[`/src/assets/cards/effects/${rank}.png`] as string}></img>
                <img id='cardTemplate' src={images[`/src/assets/cards/${rank}.png`] as string}></img>
                <div id='nameContainer'>
                    <h1 id='cardName' ref={name}>{handle}</h1>
                    <Attribute></Attribute>
                </div>
                <div id='starsContainer'>
                    {starArray}
                </div>
                <div id='imageContainer' style = {{ backgroundImage: `url(${photo})` }}></div>
                <div id='badgesContainer'>
                    {badgeArray}
                </div>
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
            {props.info && <CardInformation></CardInformation>}
        </div>
    )
}
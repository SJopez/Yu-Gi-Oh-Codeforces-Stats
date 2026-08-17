import { useEffect, useRef, useState } from 'react';
import './card.css';
import { handleSubmit, type CodeforcesUser } from './menu';
const images = import.meta.glob('/src/assets/cards/*.{png,jpg,svg}', { eager: true, import: 'default' });
const effects = import.meta.glob('/src/assets/cards/effects/*.png', { eager: true, import: 'default' });
const langIcons = import.meta.glob('/src/assets/lang/*.png', { eager: true, import: 'default' });
import Metrics from '../metrics.json';
import Langs from '../langs.json';
import Descriptions from '../assets/descriptions.json';
import html2canvas from 'html2canvas';

interface FetchProps {
    username: string;
    width: number;
    preffix: string;
    scale?: Boolean;
    info?: Boolean;
    isTopUser?: Boolean;
    topUser?: CodeforcesUser;
    rankRating: Array<CodeforcesUser>;
    contributionRank: Array<CodeforcesUser>;  
} 

interface AttributeProps {
    lang: string;
}

function Attribute(props: AttributeProps){
    type Lang = keyof typeof Langs
    const langKey = props.lang as Lang
    const path = Langs[langKey]
    
    return (
        <div id='langContainer' style={{opacity: props.lang === "" ? 0 : 1}}>
            <img src={`${langIcons[path]}`} id='attribute'></img>
            
        </div>
    )
}

export function Sparkle() {
   let spanList = []

   for (let i = 0; i < 6; i++){
       spanList.push(<span key={i}></span>)
   }
    
   return (
        <div className="sparkle">
            {spanList}
        </div>
  )
}

interface CoreProps {
    preffix: string;
    className: string;
    cardContainer: React.RefObject<HTMLDivElement | null>;
    sparkle: boolean;
    effectOpacity: number;
    effect: string;
    template: string;
    nameRef: React.RefObject<HTMLHeadingElement | null>;
    handle: string;
    lang: string;
    starArray: React.JSX.Element[];
    photo: string;
    badgeArray: React.JSX.Element[];
    type: string;
    description: string;
    maxRating: number;
    problems: number;
    loading?: Boolean
}

function Core(props: CoreProps) {
    let blur = "none"

    if (props.loading) blur = "blur(8px)"
    else blur = "none"

    return (
        <div id={props.preffix} className={props.className} ref={props.cardContainer} style={{filter: blur}}>
            {props.sparkle && <Sparkle></Sparkle>}
            <div style={{opacity: props.effectOpacity, backgroundImage: `url(${effects[`/${props.effect}`] as string})`}} id='effect'></div>
            <img id='cardTemplate' src={images[`/${props.template}`] as string}></img>
            <div id='nameContainer'>
                <h1 id='cardName' ref={props.nameRef}>{props.handle}</h1>
                <Attribute lang={props.lang}></Attribute>
            </div>
            <div id='starsContainer'>
                {props.starArray}
            </div>
            <div id='imageContainer' style = {{ backgroundImage: `url(${props.photo})` }}></div>
            <div id='badgesContainer'>
                {props.badgeArray}
            </div>
            <div id='textContainer'>
                <label id='cardType'> [{props.type}] </label>
                <div id='descriptionContainer' className='scrollable'>
                    <p id='description'>
                        {props.description}  
                    </p>
                </div>
                <hr id='separator'></hr>
                <div id='statsContainer'>
                    <label id='atk'>ATK/{props.maxRating}</label>
                    <label id='def'>DEF/{props.problems}</label>
                </div>
            </div>
        </div>
    );
}

export default function Card(props: FetchProps) {
    let starArray: React.JSX.Element[] = []
    let badgeArray: React.JSX.Element[] = []
    let name = useRef<HTMLHeadingElement>(null)
    let cardContainer = useRef<HTMLDivElement>(null)
    let blurContainer = useRef<HTMLDivElement>(null)
    let cardInfo = useRef<HTMLDivElement>(null)
    let alter = useRef<HTMLImageElement>(null)
    let [handle, setHandle] = useState("")
    let [type, setType] = useState("Legendary Grandmaster")
    let [photo, setPhoto] = useState("https://userpic.codeforces.org/422/title/50a270ed4a722867.jpg")
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
    let [problems, setProblems] = useState(0)
    let [problemsTags, setProblemsTags] = useState(Array<Array<string | number>>())
    let [description, setDescription] = useState("")
    let [template, setTemplate] = useState("src/assets/cards/legendary_grandmaster.png")
    let [effect, setEffect] = useState("src/assets/cards/effects/legendary_grandmaster.png")
    let [loading, setLoading] = useState(false)
    let [match, setMatch] = useState("")

    useEffect(() => {
        if (props.scale) setClassName("miniCardContainer")
        if (props.isTopUser) change(props.topUser!)
        else if (props.username != handle && cardContainer.current) {
            handleSubmit(props.username, change, setLoading)
        }
    }, [props.username, props.isTopUser, props.width])

    function buildDescription(user: CodeforcesUser, ratingList: Array<CodeforcesUser>, contributionList: Array<CodeforcesUser>) {
        type Legend = keyof typeof Descriptions.legends
        type RatingTop = keyof typeof Descriptions.tops.rank
        type ContriTop = keyof typeof Descriptions.tops.contribution
        type UserRank = keyof typeof Descriptions.users
        let isRatedTop = -1
        let isContriTop = -1
        let username = user.handle.toLowerCase()

        for (let i = 0; i < ratingList.length; i++){
            let rated = ratingList[i].handle.toLowerCase()
            let contri = contributionList[i].handle.toLowerCase() 
            
            if (username == rated){
                isRatedTop = i + 1
            }
            if (username == contri){
                isContriTop = i + 1
            }
        }

        let handle = user.handle
        
        if (handle in Descriptions.legends) {
            setDescription(Descriptions.legends[handle as Legend])
        }
        else if (user.rank == "headquarters"){ 
            setDescription(Descriptions.headquarters)
        }
        else if (isRatedTop > 0){
            setDescription(Descriptions.tops.rank[isRatedTop.toString() as RatingTop])
        }
        else if (isContriTop > 0){
            setDescription(Descriptions.tops.contribution[isContriTop.toString() as ContriTop])
        }
        else {
            let numIndex = Math.max(400, user.rating)
            numIndex = Math.floor(numIndex / 100) * 100
            
            let index = numIndex.toString() as UserRank
            setDescription(Descriptions.users[index])
        }
    }

   function change(user: CodeforcesUser) {
        if (user.handle === handle) return
        type Rank = keyof typeof Metrics
        const maxRankIndex = user.max_rank as Rank
        const rankIndex = user.rank as Rank
        const config = Metrics[rankIndex]
        const maxRankConfig = Metrics[maxRankIndex]
        
        setTemplate(config.card)
        setEffect(config.effect)
        setHandle(user.handle)
        setMatch(user.match_card)
        setMaxRank(user.max_rank)
        setRating(user.rating)
        setMaxRating(user.max_rating)
        setPhoto(user.avatar)
        setLang(user.most_used_lang)
        setType(config.type)
        setSparkle(config.sparkle)
        setEffectOpacity(config.effectOpacity)
        setNameEffect(config.nameEffect)
        setBadgeList(user.badges)
        setProblems(user.solved_problems)
        setProblemsTags(user.tags)
        buildDescription(user, props.rankRating, props.contributionRank)
        
        if (maxRankConfig == undefined) setStars(12)
        else setStars(maxRankConfig.stars)
        
        if (cardContainer.current) {
            setLoading(false)
        }
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
        if (props.scale && cardContainer.current){
                let scale = 0.24 * props.width / 1000
                cardContainer.current.style.setProperty("--card-scale", scale.toString());
            }
        else if (cardInfo.current && cardContainer.current && blurContainer.current && alter.current && props.width){
            if (props.width >= 408){
                cardContainer.current.style.setProperty("--card-scale", "1");
                blurContainer.current.style.setProperty("--card-scale", "1");
                cardInfo.current.style.setProperty("--card-scale", "1");
                alter.current.style.setProperty("--card-scale", "1")
            }
            else {
                let perc = (props.width / 408).toString()
                cardContainer.current.style.setProperty("--card-scale", perc);
                blurContainer.current.style.setProperty("--card-scale", perc);
                cardInfo.current.style.setProperty("--card-scale", perc);  
                alter.current.style.setProperty("--card-scale", perc)
            }        
        }

    }, [props.width, nameEffect, props.scale])
    
    for (let i = 0; i < stars; i++) {
        starArray.push(<img id={`start${i}`} key={i} className='star' src={images['/src/assets/cards/star.png'] as string}></img>)
    }
    for (let i = 0; i < badgeList.length; i++){
        badgeArray.push(<img className='badge' key={i} src={badgeList[i]}></img>)
    }

    function CardInformation() {
        let tagList = []

        for (let i = 0; i < problemsTags.length; i++){
            let tag = problemsTags[i]
            tagList.push(
                <div className="typeBanner" key={i}> 
                    <span>{tag[0]}</span>
                    <span className="typeBannerDivider"></span>
                    <span className="typeBannerCount">{tag[1]}</span>
                </div>
            )
        }

        return (
            <div className="cardInfo" ref={cardInfo}>
                <div className="username">{handle}</div>
                <div className="statsList">
                    <div className="statLine">Rank: <span className="statValue">{type}</span></div>
                    <div className="statLine">Max rank: <span className="statValue">{maxRank}</span></div>
                    <div className="statLine">Rating: <span className="statValue">{rating}</span></div>
                    <div className="statLine">Max rating: <span className="statValue">{maxRating}</span></div>
                    <div className="statLine">Problems solved: <span className="statValue">{problems}</span></div>
                    <div className="statLine">Most used lang: <span className="statValue">{lang}</span></div>
                    
                    <div className="statLine tagsLine">
                        <span className="tagsTitle">Problems tags:</span> 
                        <div className="typeBannerGrid">
                            {tagList}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    let [flip, setFlip] = useState(true)

    function saveCard() {
        if (flip) {
            if (cardContainer.current) {    
                html2canvas(cardContainer.current, 
                    {
                        onclone: (_, clonedElement) => {
                            clonedElement.style.scale = "1"; 
                            let clonedName = clonedElement.getElementsByTagName("h1")[0]
                            clonedName.classList.remove('golden')
                            clonedName.style.color = "#d4af37"

                            if (!nameEffect){
                                clonedName.style.color = "black"    
                            }
                        },
                        backgroundColor: null,
                        useCORS: true,
                    }).then(canvas => {
                    const link = document.createElement('a');
                    link.download = `${handle}.png`;
                    link.href = canvas.toDataURL();
                    link.click();
                });
            }
        }
        else if(alter.current) {
            const link = document.createElement('a');
            link.download = `match-${handle}.png`;
            link.href = match
            link.click();
        }
        
    } 

    function flipCard() {
        if (alter.current && cardContainer.current){
            if (!flip){
                cardContainer.current.classList.add('flipped')
            }
            alter.current.classList.remove('flip', 'unflip')
            cardContainer.current.classList.remove('flip', 'unflip')

            if (flip){    
                cardContainer.current.classList.add('flip')
                alter.current.classList.add('flip')
            }
            else {
                cardContainer.current.classList.add('unflip')
                alter.current.classList.add('unflip')
            }
            setTimeout(() => {
                setFlip(!flip)
            }, 500)
        }
    }

    return (
        <div className={props.preffix + 'totalContainer'}>
            {props.info ? (
                <div className='cardWrapper'>
                    <div id='blurContainer' ref={blurContainer}>
                        {loading && flip && <h1 className="loadingText"> Loading... </h1>}
                    </div>
                    <img id='alter' className='cardContainer' ref={alter} src={match}></img>
                    <Core 
                        preffix={props.preffix}
                        className={className}
                        cardContainer={cardContainer}
                        sparkle={sparkle}
                        effectOpacity={effectOpacity}
                        effect={effect}
                        template={template}
                        nameRef={name}
                        handle={handle}
                        lang={lang}
                        starArray={starArray}
                        photo={photo}
                        badgeArray={badgeArray}
                        type={type}
                        description={description}
                        maxRating={maxRating}
                        problems={problems}
                        loading={loading}
                    />
                    
                    <div className="cardActions">
                        <button className="saveCardBtn" onClick={saveCard}>
                            <svg viewBox="0 0 24 24">
                                <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
                            </svg>
                            Download Card
                        </button>
                        <button className="spinCardBtn" onClick={flipCard}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                                <path d="M3 3v5h5"></path>
                            </svg>
                        </button>
                    </div>
                    
                </div>
            ) : (
                <Core 
                    preffix={props.preffix}
                    className={className}
                    cardContainer={cardContainer}
                    sparkle={sparkle}
                    effectOpacity={effectOpacity}
                    effect={effect}
                    template={template}
                    nameRef={name}
                    handle={handle}
                    lang={lang}
                    starArray={starArray}
                    photo={photo}
                    badgeArray={badgeArray}
                    type={type}
                    description={description}
                    maxRating={maxRating}
                    problems={problems}
                />
            )}
        
            {props.info && <CardInformation></CardInformation>}
        </div>
    )
}
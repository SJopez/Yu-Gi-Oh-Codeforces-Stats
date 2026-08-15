const images = import.meta.glob('/src/assets/*.{png,jpg}', { eager: true, import: 'default' });
import { useEffect, useRef, useState } from 'react';
import Card from './card';
import './disk.css'
import { type CodeforcesUser } from './menu';

function TopContributorsBanner() {
    return (
        <div className="sectionBanner">
            <span className="sectionBannerText">Top contributors</span>
        </div>
    )
}
function TopRatingBanner() {
    let sectionBanner = useRef<HTMLDivElement>(null)
    let sectionBannerText = useRef<HTMLSpanElement>(null)
    
    useEffect(() => {
        if (sectionBanner){
            sectionBanner.current?.classList.add('red')
        }
        if (sectionBannerText){
            sectionBannerText.current?.classList.add('red')
        }
    }, [])

    return (
        <div className="sectionBanner" ref={sectionBanner}>
            <span className="sectionBannerText" ref={sectionBannerText}> Top rating  </span>
        </div>
    )
}

interface TopList {
    list: Array<CodeforcesUser>;
    subclass: string;
    title: string;
    nameSetter: (name: string) => void;
}

function TopList(props: TopList) {
    if (!props.list) return
    let slotList = []

    function searchTopUser(user: string, nameSetter: (name: string) => void) {
        window.scrollTo({top: 0, behavior:"smooth"})
        nameSetter(user)
    }

    for (let i = 0; i < props.list.length; i++){
        slotList.push(
            <div className="slotRow" key={i} onClick={() => searchTopUser(props.list[i].handle, props.nameSetter)}><span className="slotRank">{i + 1}</span><span className="slotName">{props.list[i].handle}</span></div>
        )
    }

    return (
        <div className={`topContainer ${props.subclass}`}>
            <div className="hudCorner hudCornerTopLeft" />
            <div className="hudCorner hudCornerTopRight" />
            <div className="hudCorner hudCornerBottomLeft" />
            <div className="hudCorner hudCornerBottomRight" />
            <div className="topContainerHeader">{props.title}</div>
            <div className="slotList">
                {slotList}
            </div>
        </div>
    )
}

interface DuelProps {
    width: number;
    ratingRank: Array<CodeforcesUser>;
    contributionRank: Array<CodeforcesUser>;
    nameSetter: (name: string) => void;
}

export default function DuelDisk(props: DuelProps){
    let [rankUsernameList, setRankUsernameList] = useState<Array<CodeforcesUser>>([]) 
    let [contriUsernameList, setContriUsernameList] = useState<Array<CodeforcesUser>>([])
    let rankList = []
    let contriList = []
    let yugiContainer = useRef<HTMLDivElement>(null)
    let kaibaContainer = useRef<HTMLDivElement>(null)
    let [width, setWidth] = useState(0)
    let rankTopContainer = useRef<HTMLDivElement>(null)
    let contriTopContainer = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (props.contributionRank){
            setContriUsernameList(props.contributionRank)
        }   
        if (props.ratingRank){
            setRankUsernameList(props.ratingRank)
        }
    }, [props.ratingRank, props.contributionRank])

    useEffect(() => {
        let windowWidth = props.width
        let perc = windowWidth * 0.3
        let yugi = yugiContainer.current
        let kaiba = kaibaContainer.current

        if (yugi && kaiba) {
            let value = perc + "px"

            if (windowWidth <= 800){
                value = "100%" 
            }
            
            yugi.style.width = value
            kaiba.style.width = value
            setWidth(yugi.offsetWidth)

            let rank = rankTopContainer.current
            let contri = contriTopContainer.current
           
            if (rank && contri){
                if (windowWidth > 800){
                    contri.style.width = (windowWidth - kaiba.offsetWidth - 20) + "px"
                    rank.style.width = (windowWidth - yugi.offsetWidth - 20) + "px"
                    contri.style.minHeight = kaiba.offsetHeight + "px"
                    rank.style.minHeight = yugi.offsetHeight + "px"
                }
                else {
                    rank.style.width = "100%"
                    rank.style.height = "min-content"
                    
                    contri.style.width = "100%"
                    contri.style.height = "min-content"
                }
            }   
        }    
    }, [props.width])

    if (rankUsernameList.length && contriUsernameList.length){
        for (let i = 0; i < 5; i++){
            let rankuser = rankUsernameList[i]
            let contriUser = contriUsernameList[i]
            
            rankList.push(
                <Card 
                    username={rankuser.handle}
                    preffix={`mini${i + 1}`}
                    width={width}
                    scale={true}
                    isTopUser={true}
                    topUser={rankuser}
                    rankRating={rankUsernameList}
                    contributionRank={contriUsernameList}>     
                </Card>
            )
            contriList.push(
                <Card 
                    username={contriUser.handle}
                    preffix={`mini${5 + i + 1}`}
                    width={width}
                    scale={true}
                    isTopUser={true}
                    topUser={contriUser}
                    rankRating={rankUsernameList}
                    contributionRank={contriUsernameList}>     
                </Card>
            )
        }

    }
    return (    
        <div id='duelContainer'>
            <TopRatingBanner></TopRatingBanner>
            <div id='rankContainer'>
                <div id='rankTopContainer' ref={rankTopContainer}>
                    <TopList list={rankUsernameList!} subclass='topContainerRed' title='Top 10 mundial rating' nameSetter={props.nameSetter}></TopList>
                </div>
                <div className="diskContainer" id="yugiContainer" ref={yugiContainer}>
                    <img className='diskImage' src={`${images["/src/assets/yugi.png"]}`}></img>
                    {rankList}                     
                </div>
            </div>    
            <TopContributorsBanner></TopContributorsBanner>
            <div id='contriContainer'>
                <div id='contriTopContainer' ref={contriTopContainer}>
                    <TopList list={contriUsernameList!} subclass='topContainerBlue' title='Top 10 mundial contributors' nameSetter={props.nameSetter}></TopList>
                </div>
                <div className="diskContainer" id="kaibaContainer" ref={kaibaContainer}>
                    <img className='diskImage' id='kaibaImage' src={`${images["/src/assets/kaiba.png"]}`}></img>
                    {contriList}                     
                </div>               
            </div>
        </div>
    )
}
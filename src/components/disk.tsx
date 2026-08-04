const images = import.meta.glob('/src/assets/*.{png,jpg}', { eager: true, import: 'default' });
import { useEffect, useRef, useState } from 'react';
import Card from './card';
import './disk.css'

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
    list: Array<string>;
    subclass: string;
    title: string;
}
function TopList(props: TopList) {
  let slotList = []

    for (let i = 0; i < props.list.length; i++){
        slotList.push(
            <div className="slotRow"><span className="slotRank">{i + 1}</span><span className="slotName">{props.list[i]}</span></div>
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
  );
}

interface DuelProps {
    width: number
}
interface Tops {
    rankSetter: (list: Array<string>) => void;
    contriSetter: (list: Array<string>) => void
}

async function fetchTops(rankSetter: (list: Array<string>) => void, 
                         contriSetter: (list: Array<string>) => void){
    const response = await fetch("https://yu-gi-oh-codeforces-stats.onrender.com/tops")
    if(!response.ok) throw new Error("Something went wrong!")
    const data = await response.json()
    const rank = data.top_rated as Array<string>
    const contri = data.top_contributors as Array<string>
    rankSetter(rank)
    contriSetter(contri)
}

export default function DuelDisk(props: DuelProps){
    let [rankUsernameList, setRankUsernameList] = useState(["benq", "benq", "benq", "benq", "benq", "benq", "benq", "benq", "benq", "benq"]) 
    let [contriUsernameList, setContriUsernameList] = useState(["benq", "benq", "benq", "benq", "benq", "benq", "benq", "benq", "benq", "benq"])
    let rankList = []
    let contriList = []
    let yugiContainer = useRef<HTMLDivElement>(null)
    let kaibaContainer = useRef<HTMLDivElement>(null)
    let [width, setWidth] = useState(0)
    let rankTopContainer = useRef<HTMLDivElement>(null)
    let contriTopContainer = useRef<HTMLDivElement>(null)

    useEffect(() => {
        let windowWidth = props.width
        let perc = windowWidth * 0.3
        let yugi = yugiContainer.current
        let kaiba = kaibaContainer.current
        fetchTops(setRankUsernameList, setContriUsernameList)

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
                    rank.style.width = (windowWidth - width - 20) + "px"
                    rank.style.height = yugi.offsetHeight + "px"
                    
                    contri.style.width = (windowWidth - kaiba.offsetWidth - 20) + "px"
                    contri.style.height = kaiba.offsetHeight + "px"
                }
                else {
                    rank.style.width = "100%"
                    rank.style.height = "min-content"
                    
                    contri.style.width = "100%"
                    contri.style.height = "min-content"
                }
            }   
        }    
    })

    for (let i = 0; i < 5; i++){
        let rankuser = rankUsernameList[i]
        let contriUser = contriUsernameList[i]
        
        rankList.push(
            <Card 
                username={rankuser}
                stars={1}
                preffix={`mini${i + 1}`}
                width={width}
                scale={true}>     
            </Card>
        )
        contriList.push(
            <Card 
                username={contriUser}
                stars={1}
                preffix={`mini${5 + i + 1}`}
                width={width}
                scale={true}>     
            </Card>
        )
    }

    return (    
        <div id='duelContainer'>
            <TopRatingBanner></TopRatingBanner>
            <div id='rankContainer'>
                <div id='rankTopContainer' ref={rankTopContainer}>
                    <TopList list={rankUsernameList} subclass='topContainerRed' title='Top 10 mundial rating'></TopList>
                </div>
                <div className="diskContainer" id="yugiContainer" ref={yugiContainer}>
                    <img className='diskImage' src={`${images["/src/assets/yugi.png"]}`}></img>
                    {rankList}                     
                </div>
            </div>    
            <TopContributorsBanner></TopContributorsBanner>
            <div id='contriContainer'>
                <div id='contriTopContainer' ref={contriTopContainer}>
                    <TopList list={contriUsernameList} subclass='topContainerBlue' title='Top 10 mundial contributors'></TopList>
                </div>
                <div className="diskContainer" id="kaibaContainer" ref={kaibaContainer}>
                    <img className='diskImage' id='kaibaImage' src={`${images["/src/assets/kaiba.png"]}`}></img>
                    {contriList}                     
                </div>
                
            </div>
        </div>
    )
}
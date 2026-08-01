import { useEffect, useRef, useState } from 'react'
import './App.css'
import Menu from './components/menu'

function App() {
  var container = useRef<HTMLDivElement | null>(null)
  var [width, setWidth] = useState(0)

  useEffect(() => {
      function handleResize() {
          if (container.current) {
              setWidth(container.current.offsetWidth)
          }
      }

      handleResize() 

      window.addEventListener('resize', handleResize)

      return () => {
          window.removeEventListener('resize', handleResize) 
      }
  }, [])

  return (
    <div ref={container}>
      <Menu width={width}></Menu>  
    </div>
  )
}
 
export default App


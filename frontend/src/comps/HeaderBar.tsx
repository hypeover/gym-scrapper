import React from 'react'
import { ModeToggle } from './mode-toggle'

const HeaderBar = () => {
  return (
    <div className=' w-full flex align-middle justify-end p-4' >
      <ModeToggle />
    </div>
  )
}

export default HeaderBar

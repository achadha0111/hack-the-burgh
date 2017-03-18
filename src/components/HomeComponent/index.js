import React, { Component } from 'react'
import ReactDOM, { render } from 'react-dom'
import { Link } from 'react-router'

import { Button, Input } from 'semantic-ui-react'

import './home-component.scss'

export default class HomeComponent extends Component {
  render() {
    return (
      <div className='inputForm'>
        <Input focus placeholder='Enter project URL' size='massive'/>
        <Button size='massive'>Compare</Button>
      </div>
    )
  }
}

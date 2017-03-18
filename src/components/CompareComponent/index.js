import React, { Component } from 'react'
import ReactDOM, { render } from 'react-dom'
import { Link, browserHistory } from 'react-router'

import { Button, Input } from 'semantic-ui-react'

import './home-component.scss'

export default class HomeComponent extends Component {
  
  constructor(props) {
    
    super(props)
    this.state = {
      url: null
    }

    this.handleChange = this.handleChange.bind(this)
    this.submitForm = this.submitForm.bind(this)
  }

  componentWillUpdate() {
    console.log(this.state)
  }

  handleChange(event) {
    const target = event.target
    const value  = target.value
    const name   = target.name

    this.setState({
      [name]: value
    })
  }

  submitForm() {
    browserHistory.push(`compare/${this.state.url}`)
  }


  render() {
    return (
      <div className='inputForm'>
        <Input placeholder='Enter project URL' size='massive' name='url' onChange={this.handleChange} />
        <Button onClick={this.submitForm} size='massive'>Compare</Button>
      </div>
    )
  }
}

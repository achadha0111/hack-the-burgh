import React, { Component } from 'react'
import ReactDOM, { render } from 'react-dom'
import { Link, browserHistory } from 'react-router'

import { Button, Input, Form } from 'semantic-ui-react'

import './home-component.scss'

var request = require('superagent');
var data = '..'

export default class HomeComponent extends Component {
  
  constructor(props) {
    
    super(props)
    this.state = {
      url: null,
      warning: false,
      compare: false,
      value: ''
    }

    this.handleChange = this.handleChange.bind(this)
    this.submitForm = this.submitForm.bind(this)
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
    if (this.state.url) {
      this.setState({ warning: false, compare: true })
    } else {
      this.setState({ warning: true, compare: false })
    }
  }

  renderCompare(url) {
    fetch('https://ancient-peak-64085.herokuapp.com/' + url, {
      method: 'get',
      mode: 'cors'
    }).then((response) => {
      response.json().then(data => {
        !this.state.value ? this.setState({ value: data }) : null
      })
    }).catch((err) => {
      console.error(err)
    })

    const data = this.state.value || ''
    console.log(this.state)

    return (
      <div className='compareContainer'>
        <Button className='backButton' size='medium' color='black' onClick={() => {this.setState({ compare: false, value: '' })} }>Go Back</Button>
        <div className='compareView'>
          <h1 className='projectTitle'>{data.url || '...'}</h1>
          <div className='resultsContainer'>
            <div className='result'>
              <div className='titleLine'>
                <a href='#'><h3>Bloomberg Terminal</h3></a>
                <span className='score'><div className='progressBox'><div className='progress' style={{'width': '30%'}}></div></div> 87%</span>
              </div>
              <div><span className='locationTitle'>Unihack</span></div>
              <div className='detailsContainer'>
                <div className='box'>
                  <strong>Keywords: </strong>
                  <span className='tag'>PHP</span>
                </div>
                <div className='box'>
                  <strong>Technologies: </strong>
                  <span className='tag'>PHP</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  renderForm() {
    return (
      <Form className='inputForm'>
        <Input type='url' placeholder='Enter project URL' size='massive' name='url' onChange={this.handleChange} />
        <Button type='submit' onClick={this.submitForm} size='massive'>Compare</Button>
      </Form>
    )

  }

  renderWarning() {
    console.log('display warning')
  }

  render() {
    return (
      this.state.compare && this.state.url ? this.renderCompare(this.state.url) : this.renderForm()
    )
  }
}

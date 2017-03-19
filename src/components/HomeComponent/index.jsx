import React, { Component } from 'react'
import ReactDOM, { render } from 'react-dom'
import { Link, browserHistory } from 'react-router'

import { Button, Input, Form, Segment } from 'semantic-ui-react'

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
    data ? data.reverse() : null
    console.log(this.state)

    return (
      <div className='compareContainer'>
        <Button className='backButton' size='medium' color='black' onClick={() => {this.setState({ compare: false, value: '' })} }>Go Back</Button>
        <div className='compareView'>
          <h1 className='projectTitle'>{this.state.value ? this.state.url : 'Loading...'}</h1>
          <div className='resultsContainer'>
            {data ? data.map(result => {
              let percentage = Math.round(result.similarity_score)
              return (
                <div className='result' key={ result.index }>
                  <div><span className='locationTitle'>{ result.hackathon_name }</span></div>
                  <div className='titleLine'>
                    <a href={ result.project_url }><h3>{ result.project_name }</h3></a>
                    <span className='score'><div className='progressBox'><div className='progress' style={{ 'width': `${percentage}%` }}></div></div> {percentage}%</span>
                  </div>
                  
                  <div className='detailsContainer'>
                  </div>
                </div>

              )
            }) : null}
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

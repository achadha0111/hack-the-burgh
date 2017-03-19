import React, { Component } from 'react'
import ReactDOM, { render } from 'react-dom'

import './CoreLayout.scss'

import HomeComponent from '../../components/HomeComponent'

export default class CoreLayout extends Component {
  render() {
    return (
      <div className='container'>
        <img src='./wordCloud.png' className='logo' />
        <HomeComponent />
      </div>
    )
  }
}
// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');
 
process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
 var wmat = [{'link':'https://www.geeksforgeeks.org/digital-logic-logic-gates/','img':'https://cdncontribute.geeksforgeeks.org/wp-content/uploads/logic-gates.jpg ','text':'GeeksforGeeks','rating':5},
            {'link':'https://academo.org/demos/logic-gate-simulator/','img':'https://www.elprocus.com/wp-content/uploads/2015/01/logic-gates.jpg ','text':'Academo','rating':5},
            {'link':'https://www.electronics-tutorials.ws/logic/logic_10.html ','img':'https://www.electronics-tutorials.ws/logic/log41a.gif ','text':'Electronics tutorials','rating':5},
            {'link':'http://www.ee.surrey.ac.uk/Projects/CAL/digital-logic/gatesfunc/','img':'http://www.ee.surrey.ac.uk/Projects/CAL/digital-logic/gatesfunc/graphics/symtab.gif','text':'University of Surrey','rating':5}];
  var sind = 0;
  function welcome(agent) {
    agent.add(`Hey Ramzy! What can I help you with today?`);
    //agent.add('Hello Ramzy! Let me help you study');
  }
 
  function fallback(agent) {
    //agent.add(`I didn't quite understand, Ramzy`);
    agent.add(`Yeah lol, I don't understand`);
}
 function revision(agent) {
     // Add Actions on Google library responses to your agent's response
     agent.add('jggkugugujh'); 
}
function corev(agent) {
     //var link = 'https://ajayrajnikanth.typeform.com/to/DpHnkK';
    agent.add('Don\'t miss lectures la:\n1.Logic Gates\n2.Karnaugh Maps'); // Add Actions on Google library responses to your agent's response
}
function drem(agent){
    const dtype = agent.parameters.dtype;
    if (dtype=='assignment')
    {
        agent.add('The assignemnt is due next week on Wednesday');
    }
    else if (dtype=='exam')
    {
        agent.add('The Exam timetable has not been released yet!');
    }
    else if (dtype=='test' || dtype=='midterm')
    {
        agent.add('Don\'t forget that you have a midterm on Week 7 man!');
    }
    else{
    agent.add('You\'ve finished everything already laah');
    }
}
function smwm(agent)
{
   sind = Math.floor(Math.random()*5);
    agent.add('Don\'t forget GPA is everything laah' )
    agent.add(new Card({
         title: 'Logic Gates',
         imageUrl: wmat[sind].img,
         text: wmat[sind].text,
         buttonText: 'Here is the material:',
         buttonUrl: wmat[sind].link
       })
     );
}
function fdb(agent){
    agent.add('This is gonna help a lot of other students!');
    const rater = agent.parameters.number;
    wmat[sind].rating = rater;
    
}

  // // Uncomment and edit to make your own intent handler
  // // uncomment `intentMap.set('your intent name here', yourFunctionHandler);`
  // // below to get this function to be run when a Dialogflow intent is matched
  // function yourFunctionHandler(agent) {
  //   agent.add(`This message is from Dialogflow's Cloud Functions for Firebase editor!`);
  //   agent.add(new Card({
  //       title: `Title: this is a card title`,
  //       imageUrl: 'https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png',
  //       text: `This is the body text of a card.  You can even use line\n  breaks and emoji! 💁`,
  //       buttonText: 'This is a button',
  //       buttonUrl: 'https://assistant.google.com/'
  //     })
  //   );
  //   agent.add(new Suggestion(`Quick Reply`));
  //   agent.add(new Suggestion(`Suggestion`));
  //   agent.setContext({ name: 'weather', lifespan: 2, parameters: { city: 'Rome' }});
  // }

  // // Uncomment and edit to make your own Google Assistant intent handler
  // // uncomment `intentMap.set('your intent name here', googleAssistantHandler);`
  // // below to get this function to be run when a Dialogflow intent is matched
  // function googleAssistantHandler(agent) {
  //   let conv = agent.conv(); // Get Actions on Google library conv instance
  //   conv.ask('Hello from the Actions on Google client library!') // Use Actions on Google library
  //   agent.add(conv); // Add Actions on Google library responses to your agent's response
  // }
  // // See https://github.com/dialogflow/dialogflow-fulfillment-nodejs/tree/master/samples/actions-on-google
  // // for a complete Dialogflow fulfillment library Actions on Google client library v2 integration sample

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('Revision', revision);
  intentMap.set('Course review', corev);
  intentMap.set('deadline reminder', drem);
  intentMap.set('Suggested material: website materials', smwm);
  intentMap.set('Feedback', fdb);
  // intentMap.set('your intent name here', yourFunctionHandler);
  // intentMap.set('your intent name here', googleAssistantHandler);
  agent.handleRequest(intentMap);
});

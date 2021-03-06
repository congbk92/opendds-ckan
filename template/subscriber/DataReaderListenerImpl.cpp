/*
 *
 *
 * Distributed under the OpenDDS License.
 * See: http://www.opendds.org/license.html
 */

#include <ace/Log_Msg.h>
#include <ace/OS_NS_stdlib.h>

#include "DataReaderListenerImpl.h"
#include "MessengerTypeSupportC.h"
#include "MessengerTypeSupportImpl.h"
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <cstring>
#include <sys/resource.h>

DataReaderListenerImpl::DataReaderListenerImpl(){
/*  struct rlimit rlim;
  rlim.rlim_cur = RLIM_INFINITY;
  rlim.rlim_max = RLIM_INFINITY;

  if (setrlimit(RLIMIT_MSGQUEUE, &rlim) == -1) {
    perror( "setrlimit() failed");
    exit( 1);
  }*/

  if ( -1 == ( msqid = msgget( (key_t)1234, IPC_CREAT | 0666)))
  {
    perror( "msgget() failed");
    exit( 1);
  }
/*  if (-1 == msgctl(msqid, IPC_RMID, 0))
  {
    perror( "msgctl() failed");
    exit( 1);
  }*/
}

void
DataReaderListenerImpl::on_requested_deadline_missed(
  DDS::DataReader_ptr /*reader*/,
  const DDS::RequestedDeadlineMissedStatus& /*status*/)
{
}

void
DataReaderListenerImpl::on_requested_incompatible_qos(
  DDS::DataReader_ptr /*reader*/,
  const DDS::RequestedIncompatibleQosStatus& /*status*/)
{
}

void
DataReaderListenerImpl::on_sample_rejected(
  DDS::DataReader_ptr /*reader*/,
  const DDS::SampleRejectedStatus& /*status*/)
{
}

void
DataReaderListenerImpl::on_liveliness_changed(
  DDS::DataReader_ptr /*reader*/,
  const DDS::LivelinessChangedStatus& /*status*/)
{
}

void
DataReaderListenerImpl::on_data_available(DDS::DataReader_ptr reader)
{
  Messenger::MessageDataReader_var reader_i =
    Messenger::MessageDataReader::_narrow(reader);

  if (!reader_i) {
    ACE_ERROR((LM_ERROR,
               ACE_TEXT("ERROR: %N:%l: on_data_available() -")
               ACE_TEXT(" _narrow failed!\n")));
    ACE_OS::exit(1);
  }

  Messenger::Message message;
  DDS::SampleInfo info;

  DDS::ReturnCode_t error = reader_i->take_next_sample(message, info);

  if (error == DDS::RETCODE_OK) {
/*    std::cout << "SampleInfo.sample_rank = " << info.sample_rank << std::endl;
    std::cout << "SampleInfo.instance_state = " << info.instance_state << std::endl;*/

    if (info.valid_data) {
/*      std::cout << "Message: subject    = " << message.subject.in() << std::endl
                << "         subject_id = " << message.subject_id   << std::endl
                << "         from       = " << message.from.in()    << std::endl
                << "         count      = " << message.count        << std::endl
                << "         text       = " << message.text.in()    << std::endl;*/

      rapidjson::Value val(rapidjson::kObjectType);
      rapidjson::MemoryPoolAllocator<rapidjson::CrtAllocator> alloc;
      OpenDDS::DCPS::copyToRapidJson(message, val, alloc);

      rapidjson::StringBuffer buffer;
      buffer.Clear();
      rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
      val.Accept(writer);
      std::string json_str = buffer.GetString();
      std::cout<<json_str<<std::endl;
      sendDataToQueue(json_str);
    }

  } else {
    ACE_ERROR((LM_ERROR,
               ACE_TEXT("ERROR: %N:%l: on_data_available() -")
               ACE_TEXT(" take_next_sample failed!\n")));
  }
}

void
DataReaderListenerImpl::on_subscription_matched(
  DDS::DataReader_ptr /*reader*/,
  const DDS::SubscriptionMatchedStatus& /*status*/)
{
}

void
DataReaderListenerImpl::on_sample_lost(
  DDS::DataReader_ptr /*reader*/,
  const DDS::SampleLostStatus& /*status*/)
{
}

void DataReaderListenerImpl::sendDataToQueue(std::string msg){
  t_data   data;

  sprintf( data.data_buff, "%s", msg.c_str());
  data.data_length = strlen(data.data_buff);

  if ( -1 == msgsnd( msqid, &data, sizeof(t_data), 0))
  {
    perror( "msgsnd() failed");
    exit( 1);
  }
}
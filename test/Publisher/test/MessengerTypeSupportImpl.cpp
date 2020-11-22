/* Generated by opendds_idl version 3.14 (ACE version 6.2a_p19) running on input file Messenger.idl */
#include "MessengerTypeSupportImpl.h"

#include <cstring>
#include <sstream>
#include <stdexcept>
#include "dds/DCPS/BuiltInTopicUtils.h"
#include "dds/DCPS/ContentFilteredTopicImpl.h"
#include "dds/DCPS/DataReaderImpl_T.h"
#include "dds/DCPS/DataWriterImpl_T.h"
#include "dds/DCPS/FilterEvaluator.h"
#include "dds/DCPS/MultiTopicDataReader_T.h"
#include "dds/DCPS/PoolAllocator.h"
#include "dds/DCPS/PublicationInstance.h"
#include "dds/DCPS/PublisherImpl.h"
#include "dds/DCPS/Qos_Helper.h"
#include "dds/DCPS/RakeData.h"
#include "dds/DCPS/RakeResults_T.h"
#include "dds/DCPS/RapidJsonTypeConverter.h"
#include "dds/DCPS/ReceivedDataElementList.h"
#include "dds/DCPS/Registered_Data_Types.h"
#include "dds/DCPS/Service_Participant.h"
#include "dds/DCPS/SubscriberImpl.h"
#include "dds/DCPS/Util.h"
#include "dds/DCPS/debug.h"
#include "dds/DdsDcpsDomainC.h"
#include "rapidjson/stringbuffer.h"


/* Begin MODULE: CORBA */


/* End MODULE: CORBA */


/* Begin MODULE: Messenger */



/* Begin STRUCT: Message */

OPENDDS_BEGIN_VERSIONED_NAMESPACE_DECL
namespace OpenDDS { namespace DCPS {

void gen_find_size(const Messenger::Message& stru, size_t& size, size_t& padding)
{
  ACE_UNUSED_ARG(stru);
  ACE_UNUSED_ARG(size);
  ACE_UNUSED_ARG(padding);
  find_size_ulong(size, padding);
  size += ACE_OS::strlen(stru.from.in()) + 1;
  find_size_ulong(size, padding);
  size += ACE_OS::strlen(stru.subject.in()) + 1;
  if ((size + padding) % 4) {
    padding += 4 - ((size + padding) % 4);
  }
  size += gen_max_marshaled_size(stru.subject_id);
  find_size_ulong(size, padding);
  size += ACE_OS::strlen(stru.text.in()) + 1;
  if ((size + padding) % 4) {
    padding += 4 - ((size + padding) % 4);
  }
  size += gen_max_marshaled_size(stru.count);
}

bool operator<<(Serializer& strm, const Messenger::Message& stru)
{
  ACE_UNUSED_ARG(strm);
  ACE_UNUSED_ARG(stru);
  return (strm << stru.from.in())
    && (strm << stru.subject.in())
    && (strm << stru.subject_id)
    && (strm << stru.text.in())
    && (strm << stru.count);
}

bool operator>>(Serializer& strm, Messenger::Message& stru)
{
  ACE_UNUSED_ARG(strm);
  ACE_UNUSED_ARG(stru);
  return (strm >> stru.from.out())
    && (strm >> stru.subject.out())
    && (strm >> stru.subject_id)
    && (strm >> stru.text.out())
    && (strm >> stru.count);
}

size_t gen_max_marshaled_size(const Messenger::Message& stru, bool align)
{
  ACE_UNUSED_ARG(stru);
  ACE_UNUSED_ARG(align);
  return 0;
}

size_t gen_max_marshaled_size(KeyOnly<const Messenger::Message> stru, bool align)
{
  ACE_UNUSED_ARG(stru);
  ACE_UNUSED_ARG(align);
  return 4;
}

void gen_find_size(KeyOnly<const Messenger::Message> stru, size_t& size, size_t& padding)
{
  ACE_UNUSED_ARG(stru);
  ACE_UNUSED_ARG(size);
  ACE_UNUSED_ARG(padding);
  if ((size + padding) % 4) {
    padding += 4 - ((size + padding) % 4);
  }
  size += gen_max_marshaled_size(stru.t.subject_id);
}

bool operator<<(Serializer& strm, KeyOnly<const Messenger::Message> stru)
{
  ACE_UNUSED_ARG(strm);
  ACE_UNUSED_ARG(stru);
  return (strm << stru.t.subject_id);
}

bool operator>>(Serializer& strm, KeyOnly<Messenger::Message> stru)
{
  ACE_UNUSED_ARG(strm);
  ACE_UNUSED_ARG(stru);
  return (strm >> stru.t.subject_id);
}

}  }
OPENDDS_END_VERSIONED_NAMESPACE_DECL


namespace Messenger {
::DDS::DataWriter_ptr MessageTypeSupportImpl::create_datawriter()
{
  typedef OpenDDS::DCPS::DataWriterImpl_T<Message> DataWriterImplType;
  ::DDS::DataWriter_ptr writer_impl = ::DDS::DataWriter::_nil();
  ACE_NEW_NORETURN(writer_impl,
                   DataWriterImplType());
  return writer_impl;
}

::DDS::DataReader_ptr MessageTypeSupportImpl::create_datareader()
{
  typedef OpenDDS::DCPS::DataReaderImpl_T<Message> DataReaderImplType;
  ::DDS::DataReader_ptr reader_impl = ::DDS::DataReader::_nil();
  ACE_NEW_NORETURN(reader_impl,
                   DataReaderImplType());
  return reader_impl;
}

#ifndef OPENDDS_NO_MULTI_TOPIC
::DDS::DataReader_ptr MessageTypeSupportImpl::create_multitopic_datareader()
{
  typedef OpenDDS::DCPS::DataReaderImpl_T<Message> DataReaderImplType;
  typedef OpenDDS::DCPS::MultiTopicDataReader_T<Message, DataReaderImplType> MultiTopicDataReaderImplType;
  ::DDS::DataReader_ptr multitopic_reader_impl = ::DDS::DataReader::_nil();
  ACE_NEW_NORETURN(multitopic_reader_impl,
                   MultiTopicDataReaderImplType());
  return multitopic_reader_impl;
}
#endif /* !OPENDDS_NO_MULTI_TOPIC */

#ifndef OPENDDS_NO_CONTENT_SUBSCRIPTION_PROFILE
const OpenDDS::DCPS::MetaStruct& MessageTypeSupportImpl::getMetaStructForType()
{
  return OpenDDS::DCPS::getMetaStruct<Message>();
}
#endif /* !OPENDDS_NO_CONTENT_SUBSCRIPTION_PROFILE */

bool MessageTypeSupportImpl::has_dcps_key()
{
  return TraitsType::gen_has_key ();
}

const char* MessageTypeSupportImpl::default_type_name() const
{
  return TraitsType::type_name();
}

MessageTypeSupport::_ptr_type MessageTypeSupportImpl::_narrow(CORBA::Object_ptr obj)
{
  return TypeSupportType::_narrow(obj);
}
}

#ifndef OPENDDS_NO_CONTENT_SUBSCRIPTION_PROFILE
OPENDDS_BEGIN_VERSIONED_NAMESPACE_DECL
namespace OpenDDS { namespace DCPS {

template<>
struct MetaStructImpl<Messenger::Message> : MetaStruct {
  typedef Messenger::Message T;

#ifndef OPENDDS_NO_MULTI_TOPIC
  void* allocate() const { return new T; }

  void deallocate(void* stru) const { delete static_cast<T*>(stru); }

  size_t numDcpsKeys() const { return 1; }

#endif /* OPENDDS_NO_MULTI_TOPIC */

  bool isDcpsKey(const char* field) const
  {
    if (!ACE_OS::strcmp(field, "subject_id")) {
      return true;
    }
    return false;
  }

  Value getValue(const void* stru, const char* field) const
  {
    const Messenger::Message& typed = *static_cast<const Messenger::Message*>(stru);
    ACE_UNUSED_ARG(typed);
    if (std::strcmp(field, "from") == 0) {
      return typed.from.in();
    }
    if (std::strcmp(field, "subject") == 0) {
      return typed.subject.in();
    }
    if (std::strcmp(field, "subject_id") == 0) {
      return typed.subject_id;
    }
    if (std::strcmp(field, "text") == 0) {
      return typed.text.in();
    }
    if (std::strcmp(field, "count") == 0) {
      return typed.count;
    }
    throw std::runtime_error("Field " + OPENDDS_STRING(field) + " not found or its type is not supported (in struct Messenger::Message)");
  }

  Value getValue(Serializer& ser, const char* field) const
  {
    if (std::strcmp(field, "from") == 0) {
      TAO::String_Manager val;
      if (!(ser >> val.out())) {
        throw std::runtime_error("Field 'from' could not be deserialized");
      }
      return val;
    } else {
      ACE_CDR::ULong len;
      if (!(ser >> len)) {
        throw std::runtime_error("String 'from' length could not be deserialized");
      }
      if (!ser.skip(static_cast<ACE_UINT16>(len))) {
        throw std::runtime_error("String 'from' contents could not be skipped");
      }
    }
    if (std::strcmp(field, "subject") == 0) {
      TAO::String_Manager val;
      if (!(ser >> val.out())) {
        throw std::runtime_error("Field 'subject' could not be deserialized");
      }
      return val;
    } else {
      ACE_CDR::ULong len;
      if (!(ser >> len)) {
        throw std::runtime_error("String 'subject' length could not be deserialized");
      }
      if (!ser.skip(static_cast<ACE_UINT16>(len))) {
        throw std::runtime_error("String 'subject' contents could not be skipped");
      }
    }
    if (std::strcmp(field, "subject_id") == 0) {
      ACE_CDR::Long val;
      if (!(ser >> val)) {
        throw std::runtime_error("Field 'subject_id' could not be deserialized");
      }
      return val;
    } else {
      if (!ser.skip(1, 4)) {
        throw std::runtime_error("Field 'subject_id' could not be skipped");
      }
    }
    if (std::strcmp(field, "text") == 0) {
      TAO::String_Manager val;
      if (!(ser >> val.out())) {
        throw std::runtime_error("Field 'text' could not be deserialized");
      }
      return val;
    } else {
      ACE_CDR::ULong len;
      if (!(ser >> len)) {
        throw std::runtime_error("String 'text' length could not be deserialized");
      }
      if (!ser.skip(static_cast<ACE_UINT16>(len))) {
        throw std::runtime_error("String 'text' contents could not be skipped");
      }
    }
    if (std::strcmp(field, "count") == 0) {
      ACE_CDR::Long val;
      if (!(ser >> val)) {
        throw std::runtime_error("Field 'count' could not be deserialized");
      }
      return val;
    } else {
      if (!ser.skip(1, 4)) {
        throw std::runtime_error("Field 'count' could not be skipped");
      }
    }
    if (!field[0]) {
      return 0;
    }
    throw std::runtime_error("Field " + OPENDDS_STRING(field) + " not valid for struct Messenger::Message");
  }

  ComparatorBase::Ptr create_qc_comparator(const char* field, ComparatorBase::Ptr next) const
  {
    ACE_UNUSED_ARG(next);
    if (std::strcmp(field, "from") == 0) {
      return make_field_cmp(&T::from, next);
    }
    if (std::strcmp(field, "subject") == 0) {
      return make_field_cmp(&T::subject, next);
    }
    if (std::strcmp(field, "subject_id") == 0) {
      return make_field_cmp(&T::subject_id, next);
    }
    if (std::strcmp(field, "text") == 0) {
      return make_field_cmp(&T::text, next);
    }
    if (std::strcmp(field, "count") == 0) {
      return make_field_cmp(&T::count, next);
    }
    throw std::runtime_error("Field " + OPENDDS_STRING(field) + " not found or its type is not supported (in struct Messenger::Message)");
  }

#ifndef OPENDDS_NO_MULTI_TOPIC
  const char** getFieldNames() const
  {
    static const char* names[] = {"from", "subject", "subject_id", "text", "count", 0};
    return names;
  }

  const void* getRawField(const void* stru, const char* field) const
  {
    if (std::strcmp(field, "from") == 0) {
      return &static_cast<const T*>(stru)->from;
    }
    if (std::strcmp(field, "subject") == 0) {
      return &static_cast<const T*>(stru)->subject;
    }
    if (std::strcmp(field, "subject_id") == 0) {
      return &static_cast<const T*>(stru)->subject_id;
    }
    if (std::strcmp(field, "text") == 0) {
      return &static_cast<const T*>(stru)->text;
    }
    if (std::strcmp(field, "count") == 0) {
      return &static_cast<const T*>(stru)->count;
    }
    throw std::runtime_error("Field " + OPENDDS_STRING(field) + " not found or its type is not supported (in struct Messenger::Message)");
  }

  void assign(void* lhs, const char* field, const void* rhs,
    const char* rhsFieldSpec, const MetaStruct& rhsMeta) const
  {
    ACE_UNUSED_ARG(lhs);
    ACE_UNUSED_ARG(field);
    ACE_UNUSED_ARG(rhs);
    ACE_UNUSED_ARG(rhsFieldSpec);
    ACE_UNUSED_ARG(rhsMeta);
    if (std::strcmp(field, "from") == 0) {
      static_cast<T*>(lhs)->from = *static_cast<const TAO::String_Manager*>(rhsMeta.getRawField(rhs, rhsFieldSpec));
      return;
    }
    if (std::strcmp(field, "subject") == 0) {
      static_cast<T*>(lhs)->subject = *static_cast<const TAO::String_Manager*>(rhsMeta.getRawField(rhs, rhsFieldSpec));
      return;
    }
    if (std::strcmp(field, "subject_id") == 0) {
      static_cast<T*>(lhs)->subject_id = *static_cast<const CORBA::Long*>(rhsMeta.getRawField(rhs, rhsFieldSpec));
      return;
    }
    if (std::strcmp(field, "text") == 0) {
      static_cast<T*>(lhs)->text = *static_cast<const TAO::String_Manager*>(rhsMeta.getRawField(rhs, rhsFieldSpec));
      return;
    }
    if (std::strcmp(field, "count") == 0) {
      static_cast<T*>(lhs)->count = *static_cast<const CORBA::Long*>(rhsMeta.getRawField(rhs, rhsFieldSpec));
      return;
    }
    throw std::runtime_error("Field " + OPENDDS_STRING(field) + " not found or its type is not supported (in struct Messenger::Message)");
  }
#endif /* OPENDDS_NO_MULTI_TOPIC */

  bool compare(const void* lhs, const void* rhs, const char* field) const
  {
    ACE_UNUSED_ARG(lhs);
    ACE_UNUSED_ARG(field);
    ACE_UNUSED_ARG(rhs);
    if (std::strcmp(field, "from") == 0) {
      return 0 == ACE_OS::strcmp(static_cast<const T*>(lhs)->from.in(), static_cast<const T*>(rhs)->from.in());
    }
    if (std::strcmp(field, "subject") == 0) {
      return 0 == ACE_OS::strcmp(static_cast<const T*>(lhs)->subject.in(), static_cast<const T*>(rhs)->subject.in());
    }
    if (std::strcmp(field, "subject_id") == 0) {
      return static_cast<const T*>(lhs)->subject_id == static_cast<const T*>(rhs)->subject_id;
    }
    if (std::strcmp(field, "text") == 0) {
      return 0 == ACE_OS::strcmp(static_cast<const T*>(lhs)->text.in(), static_cast<const T*>(rhs)->text.in());
    }
    if (std::strcmp(field, "count") == 0) {
      return static_cast<const T*>(lhs)->count == static_cast<const T*>(rhs)->count;
    }
    throw std::runtime_error("Field " + OPENDDS_STRING(field) + " not found or its type is not supported (in struct Messenger::Message)");
  }
};

template<>
const MetaStruct& getMetaStruct<Messenger::Message>()
{
  static MetaStructImpl<Messenger::Message> msi;
  return msi;
}

bool gen_skip_over(Serializer& ser, Messenger::Message*)
{
  ACE_UNUSED_ARG(ser);
  MetaStructImpl<Messenger::Message>().getValue(ser, "");
  return true;
}

}  }
OPENDDS_END_VERSIONED_NAMESPACE_DECL

#endif
OPENDDS_BEGIN_VERSIONED_NAMESPACE_DECL
namespace OpenDDS { namespace DCPS {

void copyToRapidJson(const Messenger::Message& src, rapidjson::Value& dst, rapidjson::Value::AllocatorType& alloc)
{
  ACE_UNUSED_ARG(src);
  ACE_UNUSED_ARG(dst);
  ACE_UNUSED_ARG(alloc);
  dst.AddMember("from", rapidjson::Value(src.from.in(), alloc).Move(), alloc);
  dst.AddMember("subject", rapidjson::Value(src.subject.in(), alloc).Move(), alloc);
  dst.AddMember("subject_id", rapidjson::Value(src.subject_id).Move(), alloc);
  dst.AddMember("text", rapidjson::Value(src.text.in(), alloc).Move(), alloc);
  dst.AddMember("count", rapidjson::Value(src.count).Move(), alloc);
}

void copyFromRapidJson(const rapidjson::Value& src, Messenger::Message& out)
{
  ACE_UNUSED_ARG(src);
  ACE_UNUSED_ARG(out);
  {
    rapidjson::Value::ConstMemberIterator it = src.FindMember("from");
    if (it != src.MemberEnd()) {
      const rapidjson::Value& val = it->value;
        if (val.IsString()) {
          out.from = val.GetString();
        }
    }
  }
  {
    rapidjson::Value::ConstMemberIterator it = src.FindMember("subject");
    if (it != src.MemberEnd()) {
      const rapidjson::Value& val = it->value;
        if (val.IsString()) {
          out.subject = val.GetString();
        }
    }
  }
  {
    rapidjson::Value::ConstMemberIterator it = src.FindMember("subject_id");
    if (it != src.MemberEnd()) {
      const rapidjson::Value& val = it->value;
        if (val.IsString()) {
          std::string ss(val.GetString());
          std::istringstream iss(ss);
          CORBA::Long temp_CORBA_Long;
          if (ss.find("0x") != std::string::npos) {
            iss >> std::hex >> temp_CORBA_Long;
          } else {
            iss >> temp_CORBA_Long;
          }
          out.subject_id = temp_CORBA_Long;
        }
        if (val.IsNumber()) {
          out.subject_id = val.GetInt();
        }
    }
  }
  {
    rapidjson::Value::ConstMemberIterator it = src.FindMember("text");
    if (it != src.MemberEnd()) {
      const rapidjson::Value& val = it->value;
        if (val.IsString()) {
          out.text = val.GetString();
        }
    }
  }
  {
    rapidjson::Value::ConstMemberIterator it = src.FindMember("count");
    if (it != src.MemberEnd()) {
      const rapidjson::Value& val = it->value;
        if (val.IsString()) {
          std::string ss(val.GetString());
          std::istringstream iss(ss);
          CORBA::Long temp_CORBA_Long;
          if (ss.find("0x") != std::string::npos) {
            iss >> std::hex >> temp_CORBA_Long;
          } else {
            iss >> temp_CORBA_Long;
          }
          out.count = temp_CORBA_Long;
        }
        if (val.IsNumber()) {
          out.count = val.GetInt();
        }
    }
  }
}

}  }
OPENDDS_END_VERSIONED_NAMESPACE_DECL


namespace Messenger {
class MessageTypeSupportRapidJsonImpl
  : public virtual MessageTypeSupportImpl
  , public virtual OpenDDS::DCPS::RapidJsonTypeConverter {

  void toRapidJson(const void* source, rapidjson::Value& dst, rapidjson::Value::AllocatorType& alloc) const
  {
    OpenDDS::DCPS::copyToRapidJson(*static_cast<const Message*>(source), dst, alloc);
  }

  void* fromRapidJson(const rapidjson::Value& source) const
  {
    Message* result = new Message();
    OpenDDS::DCPS::copyFromRapidJson(source, *result);
    return result;
  }

  void deleteFromRapidJsonResult(void* val) const
  {
    Message* delete_me = static_cast< Message*>(val);
    delete delete_me;
  }

public:
  struct Initializer {
    Initializer()
    {
      MessageTypeSupport_var ts = new MessageTypeSupportRapidJsonImpl;
      ts->register_type(0, "");
    }
  };
};

MessageTypeSupportRapidJsonImpl::Initializer init_tsrapidjson_Message;

}

/* End STRUCT: Message */

/* End MODULE: Messenger */